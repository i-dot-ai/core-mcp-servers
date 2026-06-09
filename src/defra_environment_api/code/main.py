#!/usr/bin/env python3

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

# Import all tool modules
from tools import (
    general_api,
    waste_operations,
    end_of_life_vehicles,
    enforcement_actions,
    flood_risk_activity_exemptions,
    industrial_installations,
    radioactive_substance_permits,
    scrap_metal_dealers,
    waste_exemptions,
    waste_water_carriers_brokers_dealers,
    water_discharges,
)


class DefraEnvironmentAPIRequestHandler(RequestHandler):
    """MCP Server for DEFRA Environment API access."""

    def handle_request(
        self, request: JSONRPCRequest, context: LambdaContext
    ) -> Union[JSONRPCResponse, JSONRPCError]:
        """Handle MCP JSON-RPC requests."""
        try:
            if request.method == "tools/list":
                # List available tools
                tools = [
                    {
                        "name": "search_across_registries",
                        "description": "Searches DEFRA environment API across all registries",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate (requires northing and dist)",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate (requires easting and dist)",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters (requires easting and northing)",
                                },
                            },
                            "required": [],
                            "title": "search_across_registriesArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of registry entries",
                                }
                            },
                            "required": ["result"],
                            "title": "search_across_registriesOutput",
                        },
                    },
                    {
                        "name": "simple_name_search",
                        "description": "Searches DEFRA environment API for registries that contain a given name",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "title": "Name",
                                    "description": "Name to search for",
                                },
                                "number": {
                                    "type": "string",
                                    "title": "Number",
                                    "description": "Number to search for",
                                },
                            },
                            "required": [],
                            "title": "simple_name_searchArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of matching entries",
                                }
                            },
                            "required": ["result"],
                            "title": "simple_name_searchOutput",
                        },
                    },
                    {
                        "name": "search_waste_operations",
                        "description": "Searches DEFRA environment API waste operations registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_waste_operationsArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of waste operations registrations",
                                }
                            },
                            "required": ["result"],
                            "title": "search_waste_operationsOutput",
                        },
                    },
                    {
                        "name": "search_for_waste_operation",
                        "description": "Searches DEFRA environment API waste operations registry for a particular registration by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The registration ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_waste_operationArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with waste operation details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_waste_operationOutput",
                        },
                    },
                    {
                        "name": "search_end_of_life_vehicles",
                        "description": "Searches DEFRA environment API end of life vehicles registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_end_of_life_vehiclesArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of end of life vehicle facilities",
                                }
                            },
                            "required": ["result"],
                            "title": "search_end_of_life_vehiclesOutput",
                        },
                    },
                    {
                        "name": "search_for_end_of_life_vehicle",
                        "description": "Searches DEFRA environment API end of life vehicles registry for a particular registration by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The registration ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_end_of_life_vehicleArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with facility details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_end_of_life_vehicleOutput",
                        },
                    },
                    {
                        "name": "search_enforcement_action",
                        "description": "Searches DEFRA environment API enforcement action registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "actionType": {
                                    "type": "string",
                                    "title": "Action Type",
                                    "description": "Filter by type of enforcement action",
                                },
                                "offenceType": {
                                    "type": "string",
                                    "title": "Offence Type",
                                    "description": "Filter by type of offence",
                                },
                                "agencyFunction": {
                                    "type": "string",
                                    "title": "Agency Function",
                                    "description": "Filter by agency function",
                                },
                                "after": {
                                    "type": "string",
                                    "title": "After Date",
                                    "description": "Filter actions after this date (format: DD/MM/YYYY)",
                                },
                                "before": {
                                    "type": "string",
                                    "title": "Before Date",
                                    "description": "Filter actions before this date (format: DD/MM/YYYY)",
                                },
                                "name": {
                                    "type": "string",
                                    "title": "Name",
                                    "description": "Filter by name",
                                },
                            },
                            "required": [],
                            "title": "search_enforcement_actionArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of enforcement actions",
                                }
                            },
                            "required": ["result"],
                            "title": "search_enforcement_actionOutput",
                        },
                    },
                    {
                        "name": "search_for_enforcement_action",
                        "description": "Searches DEFRA environment API enforcement action registry for a particular action by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The enforcement action ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_enforcement_actionArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with enforcement action details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_enforcement_actionOutput",
                        },
                    },
                    {
                        "name": "search_flood_risk_exemptions",
                        "description": "Searches DEFRA environment API flood risk exemptions registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                                "exemptionCode": {
                                    "type": "string",
                                    "title": "Exemption Code",
                                    "description": "Filter by exemption code",
                                },
                                "water_management_area_search": {
                                    "type": "string",
                                    "title": "Water Management Area Search",
                                    "description": "Search by water management area",
                                },
                                "name": {
                                    "type": "string",
                                    "title": "Name",
                                    "description": "Filter by name",
                                },
                                "registrationNumber": {
                                    "type": "string",
                                    "title": "Registration Number",
                                    "description": "Exact registration number",
                                },
                            },
                            "required": [],
                            "title": "search_flood_risk_exemptionsArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of flood risk exemptions",
                                }
                            },
                            "required": ["result"],
                            "title": "search_flood_risk_exemptionsOutput",
                        },
                    },
                    {
                        "name": "search_for_flood_risk_exemption",
                        "description": "Searches DEFRA environment API flood risk exemptions registry for a particular exemption by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The exemption ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_flood_risk_exemptionArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with exemption details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_flood_risk_exemptionOutput",
                        },
                    },
                    {
                        "name": "search_industrial_installations",
                        "description": "Searches DEFRA environment API industrial installations registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by permit number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_industrial_installationsArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of industrial installations",
                                }
                            },
                            "required": ["result"],
                            "title": "search_industrial_installationsOutput",
                        },
                    },
                    {
                        "name": "search_for_industrial_installation",
                        "description": "Searches DEFRA environment API industrial installations registry for a particular installation by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The installation ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_industrial_installationArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with installation details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_industrial_installationOutput",
                        },
                    },
                    {
                        "name": "search_radioactive_substance",
                        "description": "Searches DEFRA environment API radioactive substance permits registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by permit number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_radioactive_substanceArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of radioactive substance permits",
                                }
                            },
                            "required": ["result"],
                            "title": "search_radioactive_substanceOutput",
                        },
                    },
                    {
                        "name": "search_for_radioactive_substance",
                        "description": "Searches DEFRA environment API radioactive substance permits registry for a particular permit by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The permit ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_radioactive_substanceArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with permit details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_radioactive_substanceOutput",
                        },
                    },
                    {
                        "name": "search_scrap_metal_dealers",
                        "description": "Searches DEFRA environment API scrap metal dealers registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_scrap_metal_dealersArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of scrap metal dealer registrations",
                                }
                            },
                            "required": ["result"],
                            "title": "search_scrap_metal_dealersOutput",
                        },
                    },
                    {
                        "name": "search_for_scrap_metal_dealer",
                        "description": "Searches DEFRA environment API scrap metal dealers registry for a particular dealer by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The dealer ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_scrap_metal_dealerArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with dealer details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_scrap_metal_dealerOutput",
                        },
                    },
                    {
                        "name": "search_waste_exemptions",
                        "description": "Searches DEFRA environment API waste exemptions registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_waste_exemptionsArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of waste exemptions",
                                }
                            },
                            "required": ["result"],
                            "title": "search_waste_exemptionsOutput",
                        },
                    },
                    {
                        "name": "search_for_waste_exemption",
                        "description": "Searches DEFRA environment API waste exemptions registry for a particular exemption by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The exemption ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_waste_exemptionArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with exemption details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_waste_exemptionOutput",
                        },
                    },
                    {
                        "name": "search_waste_carriers_brokers",
                        "description": "Searches DEFRA environment API waste carriers and brokers registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by registration number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_waste_carriers_brokersArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of waste carrier/broker registrations",
                                }
                            },
                            "required": ["result"],
                            "title": "search_waste_carriers_brokersOutput",
                        },
                    },
                    {
                        "name": "search_for_waste_carrier_broker",
                        "description": "Searches DEFRA environment API waste carriers and brokers registry for a particular entity by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The carrier/broker ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_waste_carrier_brokerArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with carrier/broker details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_waste_carrier_brokerOutput",
                        },
                    },
                    {
                        "name": "search_water_discharges",
                        "description": "Searches DEFRA environment API water discharges registry",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "number_search": {
                                    "type": "string",
                                    "title": "Number Search",
                                    "description": "Search by permit number",
                                },
                                "name_search": {
                                    "type": "string",
                                    "title": "Name Search",
                                    "description": "Search by name",
                                },
                                "name_number_search": {
                                    "type": "string",
                                    "title": "Name/Number Search",
                                    "description": "Combined name and number search",
                                },
                                "address_search": {
                                    "type": "string",
                                    "title": "Address Search",
                                    "description": "Search by address",
                                },
                                "easting": {
                                    "type": "integer",
                                    "title": "Easting",
                                    "description": "Easting coordinate",
                                },
                                "northing": {
                                    "type": "integer",
                                    "title": "Northing",
                                    "description": "Northing coordinate",
                                },
                                "dist": {
                                    "type": "integer",
                                    "title": "Distance",
                                    "description": "Distance in meters",
                                },
                                "local_authority": {
                                    "type": "string",
                                    "title": "Local Authority",
                                    "description": "Filter by local authority",
                                },
                            },
                            "required": [],
                            "title": "search_water_dischargesArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON array of water discharge consents",
                                }
                            },
                            "required": ["result"],
                            "title": "search_water_dischargesOutput",
                        },
                    },
                    {
                        "name": "search_for_water_discharge",
                        "description": "Searches DEFRA environment API water discharges registry for a particular consent by ID",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "title": "ID",
                                    "description": "The consent ID to look up",
                                }
                            },
                            "required": ["id"],
                            "title": "search_for_water_dischargeArguments",
                        },
                        "outputSchema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "title": "Result",
                                    "description": "JSON object with consent details",
                                }
                            },
                            "required": ["result"],
                            "title": "search_for_water_dischargeOutput",
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
                if tool_name == "search_across_registries":
                    result = general_api.search_across_registries(**arguments)
                elif tool_name == "simple_name_search":
                    result = general_api.simple_name_search(**arguments)
                elif tool_name == "search_waste_operations":
                    result = waste_operations.search_waste_operations(**arguments)
                elif tool_name == "search_for_waste_operation":
                    result = waste_operations.search_for_waste_operation(**arguments)
                elif tool_name == "search_end_of_life_vehicles":
                    result = end_of_life_vehicles.search_end_of_life_vehicles(
                        **arguments
                    )
                elif tool_name == "search_for_end_of_life_vehicle":
                    result = end_of_life_vehicles.search_for_end_of_life_vehicle(
                        **arguments
                    )
                elif tool_name == "search_enforcement_action":
                    result = enforcement_actions.search_enforcement_action(**arguments)
                elif tool_name == "search_for_enforcement_action":
                    result = enforcement_actions.search_for_enforcement_action(
                        **arguments
                    )
                elif tool_name == "search_flood_risk_exemptions":
                    result = (
                        flood_risk_activity_exemptions.search_flood_risk_exemptions(
                            **arguments
                        )
                    )
                elif tool_name == "search_for_flood_risk_exemption":
                    result = (
                        flood_risk_activity_exemptions.search_for_flood_risk_exemption(
                            **arguments
                        )
                    )
                elif tool_name == "search_industrial_installations":
                    result = industrial_installations.search_industrial_installations(
                        **arguments
                    )
                elif tool_name == "search_for_industrial_installation":
                    result = (
                        industrial_installations.search_for_industrial_installation(
                            **arguments
                        )
                    )
                elif tool_name == "search_radioactive_substance":
                    result = radioactive_substance_permits.search_radioactive_substance(
                        **arguments
                    )
                elif tool_name == "search_for_radioactive_substance":
                    result = (
                        radioactive_substance_permits.search_for_radioactive_substance(
                            **arguments
                        )
                    )
                elif tool_name == "search_scrap_metal_dealers":
                    result = scrap_metal_dealers.search_scrap_metal_dealers(**arguments)
                elif tool_name == "search_for_scrap_metal_dealer":
                    result = scrap_metal_dealers.search_for_scrap_metal_dealer(
                        **arguments
                    )
                elif tool_name == "search_waste_exemptions":
                    result = waste_exemptions.search_waste_exemptions(**arguments)
                elif tool_name == "search_for_waste_exemption":
                    result = waste_exemptions.search_for_waste_exemption(**arguments)
                elif tool_name == "search_waste_carriers_brokers":
                    result = waste_water_carriers_brokers_dealers.search_waste_carriers_brokers(
                        **arguments
                    )
                elif tool_name == "search_for_waste_carrier_broker":
                    result = waste_water_carriers_brokers_dealers.search_for_waste_carrier_broker(
                        **arguments
                    )
                elif tool_name == "search_water_discharges":
                    result = water_discharges.search_water_discharges(**arguments)
                elif tool_name == "search_for_water_discharge":
                    result = water_discharges.search_for_water_discharge(**arguments)
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
                        "serverInfo": {
                            "name": "defra-environment-api",
                            "version": "1.0.0",
                        },
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
request_handler = DefraEnvironmentAPIRequestHandler()
event_handler = APIGatewayProxyEventHandler(request_handler)


def lambda_handler(event, context):
    """
    AWS Lambda handler for the DEFRA Environment API MCP server.

    This handler implements the MCP server directly without subprocess,
    avoiding any Python path issues.
    """
    return event_handler.handle(event, context)
