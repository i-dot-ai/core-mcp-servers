import requests
from urllib import parse
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_end_of_life_vehicles(
    number_search: str = None,
    name_search: str = None,
    name_number_search: str = None,
    address_search: str = None,
    easting: int = None,
    northing: int = None,
    dist: int = None,
    local_authority: str = None,
    area: str = None,
    name: str = None,
    registrationNumber: str = None,
) -> str:
    """Searches DEFRA environment API end-of-life vehicles registry"""
    try:
        url = f"{__BASE_URL}/end-of-life-vehicles/registration.json"
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
        if area:
            params["area"] = area
        if name:
            params["name"] = name
        if registrationNumber:
            params["registrationNumber"] = registrationNumber
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
                "notation": item.get("notation", None),
                "wasteManagementLicenceNumber": item.get(
                    "wasteManagementLicenceNumber", None
                ),
                "effectiveDate": item.get("effectiveDate", None),
                "issuedDate": item.get("issuedDate", None),
                "modificationDate": item.get("modificationDate", None),
                "revocationDate": item.get("revocationDate", None),
                "surrenderDate": item.get("surrenderDate", None),
                "suspensionDate": item.get("suspensionDate", None),
                "transferDate": item.get("transferDate", None),
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
                "otherLicenceNumber": item.get("otherLicenceNumber", None),
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

            # Handle area
            if item.get("area", None):
                area_obj = item.get("area")
                item_info["area"] = {
                    "id": area_obj.get("@id", None),
                    "label": area_obj.get("label", None),
                }

            # Handle sameRegistrationAs
            if item.get("sameRegistrationAs", None):
                same_reg = item.get("sameRegistrationAs")
                item_info["sameRegistrationAs"] = {
                    "register": same_reg.get("register", None),
                }

            # Handle localAuthority
            if item.get("localAuthority", None):
                local_auth = item.get("localAuthority")
                item_info["localAuthority"] = {
                    "id": local_auth.get("@id", None),
                    "label": local_auth.get("label", None),
                    "notation": local_auth.get("notation", None),
                    "otherLicenceNumber": local_auth.get("otherLicenceNumber", None),
                    "wasteManagementLicenceNumber": local_auth.get(
                        "wasteManagementLicenceNumber", None
                    ),
                }

            # Handle status
            if item.get("status", None):
                status = item.get("status")
                item_info["status"] = {
                    "id": status.get("@id", None),
                    "comment": status.get("comment", None),
                }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def search_for_end_of_life_vehicle(id: str) -> str:
    """Searches DEFRA environment API for a single end-of-life vehicle registration"""
    try:
        url = f"{__BASE_URL}/end-of-life-vehicles/registration/{id}.json"
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
                "notation": item.get("notation", None),
                "wasteManagementLicenceNumber": item.get(
                    "wasteManagementLicenceNumber", None
                ),
                "effectiveDate": item.get("effectiveDate", None),
                "issuedDate": item.get("issuedDate", None),
                "modificationDate": item.get("modificationDate", None),
                "revocationDate": item.get("revocationDate", None),
                "surrenderDate": item.get("surrenderDate", None),
                "suspensionDate": item.get("suspensionDate", None),
                "transferDate": item.get("transferDate", None),
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
                "otherLicenceNumber": item.get("otherLicenceNumber", None),
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

            # Handle area
            if item.get("area", None):
                area_obj = item.get("area")
                item_info["area"] = {
                    "id": area_obj.get("@id", None),
                    "label": area_obj.get("label", None),
                }

            # Handle sameRegistrationAs
            if item.get("sameRegistrationAs", None):
                same_reg = item.get("sameRegistrationAs")
                item_info["sameRegistrationAs"] = {
                    "register": same_reg.get("register", None),
                }

            # Handle localAuthority
            if item.get("localAuthority", None):
                local_auth = item.get("localAuthority")
                item_info["localAuthority"] = {
                    "id": local_auth.get("@id", None),
                    "label": local_auth.get("label", None),
                    "notation": local_auth.get("notation", None),
                    "otherLicenceNumber": local_auth.get("otherLicenceNumber", None),
                    "wasteManagementLicenceNumber": local_auth.get(
                        "wasteManagementLicenceNumber", None
                    ),
                }

            # Handle status
            if item.get("status", None):
                status = item.get("status")
                item_info["status"] = {
                    "id": status.get("@id", None),
                    "comment": status.get("comment", None),
                }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
