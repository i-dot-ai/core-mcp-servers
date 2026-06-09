import requests
from urllib import parse
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_waste_operations(
    number_search: str = None,
    name_search: str = None,
    name_number_search: str = None,
    address_search: str = None,
    easting: int = None,
    northing: int = None,
    dist: int = None,
    local_authority: str = None,
) -> str:
    """Searches DEFRA environment API waste operations registry"""
    try:
        url = f"{__BASE_URL}/waste-operations/registration.json"
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
        if local_authority:
            params["local-authority"] = local_authority
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
                "registerId": item.get("register", {}).get("@id", None),
                "registerName": item.get("register").get("label", None),
                "registerType": item.get("register").get("type", {}).get("@id", None),
                "registrationNumber": item.get("registrationNumber", None),
                "effectiveDate": item.get("effectiveDate", None),
                "issuedDate": item.get("issuedDate", None),
                "modificationDate": item.get("modificationDate", None),
                "revocationDate": item.get("revocationDate", None),
                "surrenderDate": item.get("surrenderDate", None),
                "suspensionDate": item.get("suspensionDate", None),
                "transferDate": item.get("transferDate", None),
                "siteAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("address", None),
                "localAuthority": item.get("localAuthority", {}).get("label", None),
                "localAuthorityId": item.get("localAuthority", {}).get("@id", None),
                "notation": item.get("notation", None),
                "otherLicenceNumber": item.get("otherLicenceNumber", None),
                "wasteManagementLicenceNumber": item.get(
                    "wasteManagementLicenceNumber", None
                ),
                "statusId": item.get("status", {}).get("@id", None),
                "statusComment": item.get("status", {}).get("comment", None),
                "distance": item.get("distance", None),
            }

            if item.get("holder", None):
                if isinstance(item.get("holder"), list):
                    for i, e in enumerate(item.get("holder")):
                        item_info["holder"][i] = e
                elif isinstance(item.get("holder"), dict):
                    item_info["holder"] = item.get("holder")
            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def search_for_waste_operation(
    id: str,
) -> str:
    """Searches DEFRA environment API waste operations registry for a particular registration"""
    try:
        url = f"{__BASE_URL}/waste-operations/registration/{id}.json"
        result = requests.get(url)
        result.raise_for_status()

        items = []

        for item in result.json()["items"]:
            item_info = {
                "registerId": item.get("register", {}).get("@id", None),
                "registerName": item.get("register").get("label", None),
                "registerType": item.get("register").get("type", {}).get("@id", None),
                "registrationNumber": item.get("registrationNumber", None),
                "effectiveDate": item.get("effectiveDate", None),
                "issuedDate": item.get("issuedDate", None),
                "modificationDate": item.get("modificationDate", None),
                "revocationDate": item.get("revocationDate", None),
                "surrenderDate": item.get("surrenderDate", None),
                "suspensionDate": item.get("suspensionDate", None),
                "transferDate": item.get("transferDate", None),
                "siteAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("address", None),
                "localAuthority": item.get("localAuthority", {}).get("label", None),
                "localAuthorityId": item.get("localAuthority", {}).get("@id", None),
                "notation": item.get("notation", None),
                "otherLicenceNumber": item.get("otherLicenceNumber", None),
                "wasteManagementLicenceNumber": item.get(
                    "wasteManagementLicenceNumber", None
                ),
                "statusId": item.get("status", {}).get("@id", None),
                "statusComment": item.get("status", {}).get("comment", None),
                "distance": item.get("distance", None),
            }

            if item.get("holder", None):
                if isinstance(item.get("holder"), list):
                    for i, e in enumerate(item.get("holder")):
                        item_info["holder"][i] = e
                elif isinstance(item.get("holder"), dict):
                    item_info["holder"] = item.get("holder")
            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
