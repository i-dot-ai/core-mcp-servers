#!/usr/bin/env python3

import wikipedia
from typing import Union
from aws_lambda_powertools.utilities.typing import LambdaContext
from mcp.types import (
    ErrorData,
    JSONRPCError,
    JSONRPCRequest,
    JSONRPCResponse,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from mcp_lambda import APIGatewayProxyEventHandler, RequestHandler


def search_for_pages(search_term: str) -> str:
    """Searches wikipedia for relevant pages"""
    try:
        search_results = wikipedia.search(search_term)
        # Convert list to string for proper JSON serialization
        return str(search_results)
    except Exception as e:
        return f"Error getting results from wikipedia: {str(e)}"


def get_page_content(page_title: str) -> str:
    """Gets full content of a specific wikipedia page based on page title"""
    try:
        page = wikipedia.page(page_title, auto_suggest=False)
        return page.content
    except Exception as e:
        return f"Error getting results from wikipedia: {str(e)}"


def summarise_page(topic: str) -> str:
    """Summarises a given wikipedia topic"""
    try:
        summary = wikipedia.summary(topic, auto_suggest=False)
        return summary
    except Exception as e:
        return f"Error getting results from wikipedia: {str(e)}"


class WikipediaRequestHandler(RequestHandler):
    """MCP Server for Wikipedia search and content retrieval."""

    def handle_request(
        self, request: JSONRPCRequest, context: LambdaContext
    ) -> Union[JSONRPCResponse, JSONRPCError]:
        """Handle MCP JSON-RPC requests."""
        try:
            if request.method == "tools/list":
                # List available tools
                tools = [
                    {
                        "name": "search_for_pages",
                        "description": "Searches wikipedia for relevant pages",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "search_term": {
                                    "type": "string",
                                    "title": "Search Term",
                                    "description": "The search term to search for on Wikipedia",
                                }
                            },
                            "required": ["search_term"],
                            "title": "search_for_pagesArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "List of Wikipedia page titles matching the search term",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_pagesOutput",
                        },
                    },
                    {
                        "name": "get_page_content",
                        "description": "Gets information about a specific page based on page title",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "page_title": {
                                    "type": "string",
                                    "title": "Page Title",
                                    "description": "The title of the Wikipedia page to retrieve",
                                }
                            },
                            "required": ["page_title"],
                            "title": "get_page_contentArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "Full content of the Wikipedia page",
                                }
                            },
                            "required": ["result"],
                            "title": "get_page_contentOutput",
                        },
                    },
                    {
                        "name": "summarise_page",
                        "description": "Summarises a given wikipedia topic",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {
                                    "type": "string",
                                    "title": "Topic",
                                    "description": "The Wikipedia topic to summarize",
                                }
                            },
                            "required": ["topic"],
                            "title": "summarise_pageArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "Summary of the Wikipedia topic",
                                }
                            },
                            "required": ["result"],
                            "title": "summarise_pageOutput",
                        },
                    },
                ]

                return JSONRPCResponse(
                    jsonrpc="2.0",
                    result={"tools": tools},
                    id=request.id,
                )

            elif request.method == "tools/call":
                # Handle tool call
                if not request.params:
                    return JSONRPCError(
                        jsonrpc="2.0",
                        error=ErrorData(
                            code=INVALID_PARAMS, message="Missing parameters"
                        ),
                        id=request.id,
                    )

                tool_name = request.params.get("name")
                arguments = request.params.get("arguments", {})

                # Execute the appropriate tool
                if tool_name == "search_for_pages":
                    search_term = arguments.get("search_term")
                    if not search_term:
                        return JSONRPCError(
                            jsonrpc="2.0",
                            error=ErrorData(
                                code=INVALID_PARAMS,
                                message="search_term parameter is required",
                            ),
                            id=request.id,
                        )
                    result = search_for_pages(search_term)

                elif tool_name == "get_page_content":
                    page_title = arguments.get("page_title")
                    if not page_title:
                        return JSONRPCError(
                            jsonrpc="2.0",
                            error=ErrorData(
                                code=INVALID_PARAMS,
                                message="page_title parameter is required",
                            ),
                            id=request.id,
                        )
                    result = get_page_content(page_title)

                elif tool_name == "summarise_page":
                    topic = arguments.get("topic")
                    if not topic:
                        return JSONRPCError(
                            jsonrpc="2.0",
                            error=ErrorData(
                                code=INVALID_PARAMS,
                                message="topic parameter is required",
                            ),
                            id=request.id,
                        )
                    result = summarise_page(topic)

                else:
                    return JSONRPCError(
                        jsonrpc="2.0",
                        error=ErrorData(
                            code=INVALID_PARAMS, message=f"Unknown tool: {tool_name}"
                        ),
                        id=request.id,
                    )

                return JSONRPCResponse(
                    jsonrpc="2.0",
                    result={
                        "content": [{"type": "text", "text": result}],
                        "structuredContent": {"result": result},
                        "isError": False,
                    },
                    id=request.id,
                )

            elif request.method == "initialize":
                # Handle initialization
                return JSONRPCResponse(
                    jsonrpc="2.0",
                    result={
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "wikipedia", "version": "1.0.0"},
                    },
                    id=request.id,
                )

            elif request.method == "ping":
                # Handle ping
                return JSONRPCResponse(
                    jsonrpc="2.0",
                    result={},
                    id=request.id,
                )

            else:
                return JSONRPCError(
                    jsonrpc="2.0",
                    error=ErrorData(
                        code=-32601, message=f"Method not found: {request.method}"
                    ),
                    id=request.id,
                )

        except Exception as e:
            return JSONRPCError(
                jsonrpc="2.0",
                error=ErrorData(code=INTERNAL_ERROR, message=str(e)),
                id=request.id,
            )


# Create the request handler and event handler
request_handler = WikipediaRequestHandler()
event_handler = APIGatewayProxyEventHandler(request_handler)


def lambda_handler(event, context):
    """
    AWS Lambda handler for the Wikipedia MCP server.

    This handler implements the MCP server directly without subprocess,
    avoiding any Python path issues.
    """
    return event_handler.handle(event, context)
