import requests
from urllib import parse
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_across_registries(
    number_search: str = None,
    name_search: str = None,
    name_number_search: str = None,
    address_search: str = None,
    easting: int = None,
    northing: int = None,
    dist: int = None,
) -> str:
    """Searches DEFRA environment API across all registries"""
    try:
        url = f"{__BASE_URL}/api/search.json"
        params = {}
        if number_search:
            params["number-search"] = number_search
        if name_search:
            params["name-search"] = name_search
        if name_number_search:
            params["name-number-search"] = name_number_search
        if address_search:
            params["address-search"] = address_search
        if easting and northing and dist:
            params["easting"] = easting
            params["northing"] = northing
            params["dist"] = dist
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
                "register_id": item.get("register", {}).get("@id", None),
                "register_name": item.get("register").get("label", None),
                "registration_number": item.get("registrationNumber", None),
                "expiryDate": item.get("expiryDate", None),
                "registrationDate": item.get("registrationDate", None),
                "siteAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("address", None),
                "localAuthority": item.get("localAuthority", {}).get("label", None),
                "distance": item.get("distance", None),
            }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def simple_name_search(
    name: str = None,
    number: str = None,
) -> str:
    """Searches DEFRA environment API for registries that contain a given name"""
    try:
        url = f"{__BASE_URL}/api/search.json"
        params = {}
        if name:
            params["name"] = name
        if number:
            params["number"] = number
        if not params:
            return "No search term parameters were provided so no search has been performed"
        params["infix"] = True
        parsed_params = parse.urlencode(params)
        parsed_url = f"{url}?%s" % parsed_params
        result = requests.get(parsed_url)
        result.raise_for_status()

        return result.json()

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
