import requests
from urllib import parse
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_water_discharges(
    number_search: str = None,
    name_search: str = None,
    name_number_search: str = None,
    address_search: str = None,
    easting: int = None,
    northing: int = None,
    dist: int = None,
    local_authority: str = None,
) -> str:
    """Searches DEFRA environment API water discharges registry"""
    try:
        url = f"{__BASE_URL}/water-discharges/registration.json"
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
                "registerName": item.get("register", {}).get("label", None),
                "registerType": item.get("register", {})
                .get("type", {})
                .get("@id", None),
                "registrationNumber": item.get("registrationNumber", None),
                "type": item.get("type", None),
                "effectiveDate": item.get("effectiveDate", None),
                "revocationDate": item.get("revocationDate", None),
                "localAuthority": item.get("localAuthority", {}).get("label", None),
                "localAuthorityId": item.get("localAuthority", {}).get("@id", None),
                "notation": item.get("notation", None),
                "siteId": item.get("site", {}).get("@id", None),
                "siteAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("address", None),
                "postcode": item.get("site", {})
                .get("siteAddress", {})
                .get("postcode", None),
                "organizationName": item.get("site", {})
                .get("siteAddress", {})
                .get("organization_name", None),
                "streetAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("street_address", None),
                "locality": item.get("site", {})
                .get("siteAddress", {})
                .get("locality", None),
                "postcodeURI": item.get("site", {})
                .get("siteAddress", {})
                .get("postcodeURI", None),
                "distance": item.get("distance", None),
            }

            # Handle holder (can be single object or array)
            if item.get("holder", None):
                if isinstance(item.get("holder"), list):
                    item_info["holder"] = []
                    for holder in item.get("holder"):
                        holder_info = {
                            "id": holder.get("@id", None),
                            "name": holder.get("name", None),
                            "tradingName": holder.get("tradingName", None),
                            "type": holder.get("type", None),
                        }
                        item_info["holder"].append(holder_info)
                elif isinstance(item.get("holder"), dict):
                    holder = item.get("holder")
                    item_info["holder"] = {
                        "id": holder.get("@id", None),
                        "name": holder.get("name", None),
                        "tradingName": holder.get("tradingName", None),
                        "type": holder.get("type", None),
                    }

            # Handle effluent type
            if item.get("effluentType", None):
                effluent = item.get("effluentType")
                item_info["effluentType"] = {
                    "id": effluent.get("@id", None),
                    "comment": effluent.get("comment", None),
                }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def search_for_water_discharge(
    id: str,
) -> str:
    """Searches DEFRA environment API water discharges registry for a particular registration"""
    try:
        url = f"{__BASE_URL}/water-discharges/registration/{id}.json"
        result = requests.get(url)
        result.raise_for_status()

        items = []

        for item in result.json()["items"]:
            item_info = {
                "registerId": item.get("register", {}).get("@id", None),
                "registerName": item.get("register", {}).get("label", None),
                "registerType": item.get("register", {})
                .get("type", {})
                .get("@id", None),
                "registrationNumber": item.get("registrationNumber", None),
                "type": item.get("type", None),
                "effectiveDate": item.get("effectiveDate", None),
                "revocationDate": item.get("revocationDate", None),
                "localAuthority": item.get("localAuthority", {}).get("label", None),
                "localAuthorityId": item.get("localAuthority", {}).get("@id", None),
                "notation": item.get("notation", None),
                "siteId": item.get("site", {}).get("@id", None),
                "siteAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("address", None),
                "postcode": item.get("site", {})
                .get("siteAddress", {})
                .get("postcode", None),
                "organizationName": item.get("site", {})
                .get("siteAddress", {})
                .get("organization_name", None),
                "streetAddress": item.get("site", {})
                .get("siteAddress", {})
                .get("street_address", None),
                "locality": item.get("site", {})
                .get("siteAddress", {})
                .get("locality", None),
                "postcodeURI": item.get("site", {})
                .get("siteAddress", {})
                .get("postcodeURI", None),
                "distance": item.get("distance", None),
            }

            # Handle holder (can be single object or array)
            if item.get("holder", None):
                if isinstance(item.get("holder"), list):
                    item_info["holder"] = []
                    for holder in item.get("holder"):
                        holder_info = {
                            "id": holder.get("@id", None),
                            "name": holder.get("name", None),
                            "tradingName": holder.get("tradingName", None),
                            "type": holder.get("type", None),
                        }
                        item_info["holder"].append(holder_info)
                elif isinstance(item.get("holder"), dict):
                    holder = item.get("holder")
                    item_info["holder"] = {
                        "id": holder.get("@id", None),
                        "name": holder.get("name", None),
                        "tradingName": holder.get("tradingName", None),
                        "type": holder.get("type", None),
                    }

            # Handle effluent type
            if item.get("effluentType", None):
                effluent = item.get("effluentType")
                item_info["effluentType"] = {
                    "id": effluent.get("@id", None),
                    "comment": effluent.get("comment", None),
                }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
