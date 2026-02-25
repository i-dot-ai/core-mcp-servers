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


def search_gov_uk_acronyms(acronym: str) -> str:
    """
    Search for UK government acronyms using the Tools for Civil Servants website.

    Args:
        acronym: The acronym to search for

    Returns:
        A formatted string with the acronym meaning and definition
    """
    try:
        url = "https://acronyms.toolsforcivilservants.co.uk"

        # Make request with proper headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # Parse acronyms from table headers
        acronyms = [
            m.strip()
            for m in re.findall(
                r'<th\s+scope="row" class="govuk-table__header">(.*?)</th>',
                html,
                flags=re.S,
            )
        ]

        # Parse information from table cells
        info = [
            m.strip()
            for m in re.findall(
                r'<td\s+class="govuk-table__cell">(.*?)</td>', html, flags=re.S
            )
        ]

        # Process the data (assuming 4 columns: meaning, definition, department, team)
        ITEMS_PER_ROW = 4
        data = {}

        for index, acro in enumerate(acronyms):
            try:
                if index * ITEMS_PER_ROW + 3 < len(info):
                    data[acro.upper()] = {
                        "acronym": acro,
                        "meaning": info[index * ITEMS_PER_ROW].strip(),
                        "definition": info[(index * ITEMS_PER_ROW) + 1].strip(),
                        "department": info[(index * ITEMS_PER_ROW) + 2].strip(),
                        "team": info[(index * ITEMS_PER_ROW) + 3].strip(),
                    }
            except IndexError:
                # Skip if data is incomplete
                continue

        # Look for the acronym (case insensitive)
        acronym_upper = acronym.upper()
        if acronym_upper not in data:
            # Try partial matches
            partial_matches = [
                key
                for key in data.keys()
                if acronym_upper in key or key in acronym_upper
            ]
            if partial_matches:
                matches_info = []
                for match in partial_matches[:3]:  # Limit to 3 matches
                    match_data = data[match]
                    matches_info.append(
                        f"{match_data['acronym']}: {match_data['meaning']}"
                    )
                return (
                    f"No exact match found for '{acronym}'. Similar acronyms:\n"
                    + "\n".join(matches_info)
                )
            else:
                return f"No definition found for acronym '{acronym}'. The acronym may not be in the UK government database."

        match = data[acronym_upper]

        # Format response
        response_parts = [f"{match['acronym']} stands for {match['meaning']}."]

        if match["definition"]:
            response_parts.append(f"Definition: {match['definition']}")

        if match["department"]:
            response_parts.append(f"Department: {match['department']}")

        if match["team"]:
            response_parts.append(f"Team: {match['team']}")

        return " ".join(response_parts)

    except requests.RequestException as e:
        return f"Error fetching data from UK government acronyms database: {str(e)}"
    except Exception as e:
        return f"Error processing acronym lookup: {str(e)}"


class GovUKAcronymsRequestHandler(RequestHandler):
    """MCP Server for UK Government Acronyms lookup."""

    def handle_request(
        self, request: JSONRPCRequest, context: LambdaContext
    ) -> Union[JSONRPCResponse, JSONRPCError]:
        """Handle MCP JSON-RPC requests."""
        try:
            if request.method == "tools/list":
                # List available tools
                tools = [
                    {
                        "name": "search_gov_uk_acronym",
                        "description": "Search for the meaning of UK government acronyms",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "acronym": {
                                    "type": "string",
                                    "title": "Acronym",
                                    "description": "The acronym to search for (e.g., DfE, HMRC, NHS)",
                                }
                            },
                            "required": ["acronym"],
                            "title": "search_gov_uk_acronymArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "The meaning and details of the acronym",
                                }
                            },
                            "required": ["result"],
                            "title": "search_gov_uk_acronymOutput",
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
                if tool_name != "search_gov_uk_acronym":
                    return JSONRPCError(
                        jsonrpc="2.0",
                        error=ErrorData(
                            code=INVALID_PARAMS, message=f"Unknown tool: {tool_name}"
                        ),
                        id=request.id,
                    )

                arguments = request.params.get("arguments", {})
                acronym = arguments.get("acronym")
                if not acronym:
                    return JSONRPCError(
                        jsonrpc="2.0",
                        error=ErrorData(
                            code=INVALID_PARAMS, message="acronym parameter is required"
                        ),
                        id=request.id,
                    )

                # Execute the tool
                result = search_gov_uk_acronyms(acronym)

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
                        "serverInfo": {"name": "gov-uk-acronyms", "version": "1.0.0"},
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
request_handler = GovUKAcronymsRequestHandler()
event_handler = APIGatewayProxyEventHandler(request_handler)


def lambda_handler(event, context):
    """
    AWS Lambda handler for the Gov UK Acronyms MCP server.

    This handler implements the MCP server directly without subprocess,
    avoiding any Python path issues.
    """
    return event_handler.handle(event, context)
