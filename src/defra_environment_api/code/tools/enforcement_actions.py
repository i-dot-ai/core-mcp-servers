import requests
from urllib import parse
from dateutil import parser
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_enforcement_action(
    name_search: str = None,
    actionType: str = None,
    offenceType: str = None,
    agencyFunction: str = None,
    after: str = None,
    before: str = None,
    name: str = None,
) -> str:
    """Searches DEFRA environment API enforcement action registry"""
    try:
        url = f"{__BASE_URL}/enforcement-action/registration.json"
        params = {}
        if name_search:
            params["name-search"] = name_search
        if actionType:
            params["actionType"] = actionType
        if offenceType:
            params["offenceType"] = offenceType
        if agencyFunction:
            params["agencyFunction"] = agencyFunction
        if after:
            parsed_date = parser.parse(after, dayfirst=True)
            params["after"] = parsed_date.strftime("%d/%m/%Y")
        if before:
            parsed_date = parser.parse(before, dayfirst=True)
            params["before"] = parsed_date.strftime("%d/%m/%Y")
        if name:
            params["name"] = name
        if not params:
            return "No search term parameters were provided so no search has been performed"
        params["_limit"] = 10
        parsed_params = parse.urlencode(params)
        parsed_url = f"{url}?%s" % parsed_params
        result = requests.get(parsed_url)
        result.raise_for_status()

        items = []

        for item in result.json()["items"]:
            item_info = {
                "notation": item.get("notation", None),
                "actionDate": item.get("actionDate", None),
                "register": item.get("register", None),
            }

            # Handle offender
            if item.get("offender", None):
                offender = item.get("offender")
                item_info["offender"] = {
                    "id": offender.get("@id", None),
                    "name": offender.get("name", None),
                }

                # Handle offender address
                if offender.get("hasAddress", None):
                    address = offender.get("hasAddress")
                    item_info["offender"]["hasAddress"] = {
                        "id": address.get("@id", None),
                        "address": address.get("address", None),
                    }

            # Handle offence (can be single object or array)
            if item.get("offence", None):
                offence = item.get("offence")
                if isinstance(offence, list):
                    item_info["offence"] = []
                    for off in offence:
                        offence_info = {
                            "id": off.get("@id", None),
                            "legislationTitle": off.get("legislationTitle", None),
                        }

                        # Handle action type
                        if off.get("actionType", None):
                            action_type = off.get("actionType")
                            offence_info["actionType"] = {
                                "id": action_type.get("@id", None),
                                "prefLabel": action_type.get("prefLabel", None),
                            }

                        # Handle agency function
                        if off.get("agencyFunction", None):
                            agency_func = off.get("agencyFunction")
                            offence_info["agencyFunction"] = {
                                "id": agency_func.get("@id", None),
                                "prefLabel": agency_func.get("prefLabel", None),
                            }

                        item_info["offence"].append(offence_info)
                elif isinstance(offence, dict):
                    item_info["offence"] = {
                        "id": offence.get("@id", None),
                        "legislationTitle": offence.get("legislationTitle", None),
                    }

                    # Handle action type
                    if offence.get("actionType", None):
                        action_type = offence.get("actionType")
                        item_info["offence"]["actionType"] = {
                            "id": action_type.get("@id", None),
                            "prefLabel": action_type.get("prefLabel", None),
                        }

                    # Handle agency function
                    if offence.get("agencyFunction", None):
                        agency_func = offence.get("agencyFunction")
                        item_info["offence"]["agencyFunction"] = {
                            "id": agency_func.get("@id", None),
                            "prefLabel": agency_func.get("prefLabel", None),
                        }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def search_for_enforcement_action(
    id: str,
) -> str:
    """Searches DEFRA environment API enforcement action registry for a particular action"""
    try:
        url = f"{__BASE_URL}/enforcement-action/registration/{id}.json"
        result = requests.get(url)
        result.raise_for_status()

        items = []

        for item in result.json()["items"]:
            item_info = {
                "notation": item.get("notation", None),
                "actionDate": item.get("actionDate", None),
                "register": item.get("register", None),
            }

            # Handle offender
            if item.get("offender", None):
                offender = item.get("offender")
                item_info["offender"] = {
                    "id": offender.get("@id", None),
                    "name": offender.get("name", None),
                }

                # Handle offender address
                if offender.get("hasAddress", None):
                    address = offender.get("hasAddress")
                    item_info["offender"]["hasAddress"] = {
                        "id": address.get("@id", None),
                        "address": address.get("address", None),
                    }

            # Handle offence (can be single object or array)
            if item.get("offence", None):
                offence = item.get("offence")
                if isinstance(offence, list):
                    item_info["offence"] = []
                    for off in offence:
                        offence_info = {
                            "id": off.get("@id", None),
                            "legislationTitle": off.get("legislationTitle", None),
                        }

                        # Handle action type
                        if off.get("actionType", None):
                            action_type = off.get("actionType")
                            offence_info["actionType"] = {
                                "id": action_type.get("@id", None),
                                "prefLabel": action_type.get("prefLabel", None),
                            }

                        # Handle agency function
                        if off.get("agencyFunction", None):
                            agency_func = off.get("agencyFunction")
                            offence_info["agencyFunction"] = {
                                "id": agency_func.get("@id", None),
                                "prefLabel": agency_func.get("prefLabel", None),
                            }

                        item_info["offence"].append(offence_info)
                elif isinstance(offence, dict):
                    item_info["offence"] = {
                        "id": offence.get("@id", None),
                        "legislationTitle": offence.get("legislationTitle", None),
                    }

                    # Handle action type
                    if offence.get("actionType", None):
                        action_type = offence.get("actionType")
                        item_info["offence"]["actionType"] = {
                            "id": action_type.get("@id", None),
                            "prefLabel": action_type.get("prefLabel", None),
                        }

                    # Handle agency function
                    if offence.get("agencyFunction", None):
                        agency_func = offence.get("agencyFunction")
                        item_info["offence"]["agencyFunction"] = {
                            "id": agency_func.get("@id", None),
                            "prefLabel": agency_func.get("prefLabel", None),
                        }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
