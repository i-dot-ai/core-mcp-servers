import requests
from urllib import parse
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_waste_carriers_brokers(
    number_search: str = None,
    name_search: str = None,
    name_number_search: str = None,
    address_search: str = None,
    easting: int = None,
    northing: int = None,
    dist: int = None,
    local_authority: str = None,
) -> str:
    """Searches DEFRA environment API waste carriers brokers registry"""
    try:
        url = f"{__BASE_URL}/waste-carriers-brokers/registration.json"
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
                "registrationDate": item.get("registrationDate", None),
                "expiryDate": item.get("expiryDate", None),
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
                "distance": item.get("location", {}).get("distance", None),
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

            # Handle applicant type
            if item.get("applicantType", None):
                applicant_type = item.get("applicantType")
                item_info["applicantType"] = {
                    "id": applicant_type.get("@id", None),
                    "prefLabel": applicant_type.get("prefLabel", None),
                }

            # Handle registration type
            if item.get("registrationType", None):
                registration_type = item.get("registrationType")
                item_info["registrationType"] = {
                    "id": registration_type.get("@id", None),
                    "notation": registration_type.get("notation", None),
                    "label": registration_type.get("label", None),
                    "prefLabel": registration_type.get("prefLabel", None),
                }

            # Handle tier
            if item.get("tier", None):
                tier = item.get("tier")
                item_info["tier"] = {
                    "id": tier.get("@id", None),
                    "label": tier.get("label", None),
                }

            # Handle regime
            if item.get("regime", None):
                regime = item.get("regime")
                item_info["regime"] = {
                    "id": regime.get("@id", None),
                    "prefLabel": regime.get("prefLabel", None),
                }

            # Handle seeAlso (can be URI or object)
            if item.get("seeAlso", None):
                see_also = item.get("seeAlso")
                if isinstance(see_also, str):
                    item_info["seeAlso"] = see_also
                elif isinstance(see_also, dict):
                    item_info["seeAlso"] = {
                        "id": see_also.get("@id", None),
                    }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def search_for_waste_carrier_broker(
    id: str,
) -> str:
    """Searches DEFRA environment API waste carriers brokers registry for a particular registration"""
    try:
        url = f"{__BASE_URL}/waste-carriers-brokers/registration/{id}.json"
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
                "registrationDate": item.get("registrationDate", None),
                "expiryDate": item.get("expiryDate", None),
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
                "distance": item.get("location", {}).get("distance", None),
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

            # Handle applicant type
            if item.get("applicantType", None):
                applicant_type = item.get("applicantType")
                item_info["applicantType"] = {
                    "id": applicant_type.get("@id", None),
                    "prefLabel": applicant_type.get("prefLabel", None),
                }

            # Handle registration type
            if item.get("registrationType", None):
                registration_type = item.get("registrationType")
                item_info["registrationType"] = {
                    "id": registration_type.get("@id", None),
                    "notation": registration_type.get("notation", None),
                    "label": registration_type.get("label", None),
                    "prefLabel": registration_type.get("prefLabel", None),
                }

            # Handle tier
            if item.get("tier", None):
                tier = item.get("tier")
                item_info["tier"] = {
                    "id": tier.get("@id", None),
                    "label": tier.get("label", None),
                }

            # Handle regime
            if item.get("regime", None):
                regime = item.get("regime")
                item_info["regime"] = {
                    "id": regime.get("@id", None),
                    "prefLabel": regime.get("prefLabel", None),
                }

            # Handle seeAlso (can be URI or object)
            if item.get("seeAlso", None):
                see_also = item.get("seeAlso")
                if isinstance(see_also, str):
                    item_info["seeAlso"] = see_also
                elif isinstance(see_also, dict):
                    item_info["seeAlso"] = {
                        "id": see_also.get("@id", None),
                    }

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
