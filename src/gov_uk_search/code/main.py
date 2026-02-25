#!/usr/bin/env python3

import json
import re
import requests
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


def extract_body_content(html_content: str) -> str:
    """Extract content from gov.uk main content area using simple regex"""

    # I used the `main` area rather than body to limit the hidden elements included
    main_match = re.search(
        r'<main[^>]*role="main"[^>]*id="content"[^>]*class="govuk-main-wrapper[^"]*"[^>]*>(.*?)</main>',
        html_content,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if main_match:
        return main_match.group(1).strip()
    else:
        # Fallback to trying main without the extra attributes
        fallback_match = re.search(
            r'<main[^>]*role="main"[^>]*>(.*?)</main>',
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        if fallback_match:
            return fallback_match.group(1).strip()
        else:
            # If no main tag found, return the whole content
            return html_content


def scrape_url(url: str) -> str:
    """Scrape a single URL and return `main` content"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        body_content = extract_body_content(response.text)

        return body_content

    except Exception as e:
        return f"Error scraping page: {str(e)}"


def search_gov_uk(search_term: str) -> str:
    """Searches the gov.uk website for 5 pages related to the given query and returns raw HTML body content"""

    search_url = "https://www.gov.uk/api/search.json"
    params = {
        "q": search_term,
        "count": 5,  # Limited to 5 for processing speed as async isn't possible without using a container
        "fields": "link",  # Link field just gets back the slug for the page, e.g. `/estimate-income-tax`
    }

    try:
        response = requests.get(search_url, params=params, timeout=20)
        response.raise_for_status()
        search_data = response.json()

        if not search_data.get("results"):
            return f"No results found for search term: {search_term}"

        # Extract URLs to scrape
        urls_to_scrape = []
        for result in search_data["results"]:
            link = result.get("link", "")
            # Temporarily ignore full web links until we work out how to deal with that
            if link and not link.startswith("https://"):
                full_url = f"https://www.gov.uk{link}"
                urls_to_scrape.append(full_url)

        if not urls_to_scrape:
            return f"No valid links found in search results for: {search_term}"

        # Scrape each URL synchronously
        scraped_data = []
        for url in urls_to_scrape:
            result = scrape_url(url)
            scraped_data.append(result)

        # Return as JSON string
        return json.dumps(scraped_data, indent=2)

    except requests.RequestException as e:
        return f"Error searching gov.uk: {str(e)}"
    except Exception as e:
        return f"Error processing search results: {str(e)}"


class GovUKSearchRequestHandler(RequestHandler):
    """MCP Server for UK Government website search."""

    def handle_request(
        self, request: JSONRPCRequest, context: LambdaContext
    ) -> Union[JSONRPCResponse, JSONRPCError]:
        """Handle MCP JSON-RPC requests."""
        try:
            if request.method == "tools/list":
                # List available tools
                tools = [
                    {
                        "name": "search_gov_uk",
                        "description": "Searches the gov.uk website for 5 pages and returns raw HTML body content",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "search_term": {
                                    "type": "string",
                                    "title": "Search Term",
                                    "description": "The search term to search for on gov.uk",
                                }
                            },
                            "required": ["search_term"],
                            "title": "search_gov_ukArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON string containing scraped content from gov.uk pages",
                                }
                            },
                            "required": ["result"],
                            "title": "search_gov_ukOutput",
                        },
                    }
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
                if tool_name != "search_gov_uk":
                    return JSONRPCError(
                        jsonrpc="2.0",
                        error=ErrorData(
                            code=INVALID_PARAMS, message=f"Unknown tool: {tool_name}"
                        ),
                        id=request.id,
                    )

                arguments = request.params.get("arguments", {})
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

                # Execute the tool
                result = search_gov_uk(search_term)

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
                        "serverInfo": {"name": "gov-uk-search", "version": "1.0.0"},
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
request_handler = GovUKSearchRequestHandler()
event_handler = APIGatewayProxyEventHandler(request_handler)


def lambda_handler(event, context):
    """
    AWS Lambda handler for the Gov UK Search MCP server.

    This handler implements the MCP server directly without subprocess,
    avoiding any Python path issues.
    """
    return event_handler.handle(event, context)
