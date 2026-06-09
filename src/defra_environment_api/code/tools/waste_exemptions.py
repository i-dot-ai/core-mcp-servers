import requests
from urllib import parse
import json

__BASE_URL = "https://environment.data.gov.uk/public-register"


def search_waste_exemptions(
    number_search: str = None,
    name_search: str = None,
    name_number_search: str = None,
    address_search: str = None,
    easting: int = None,
    northing: int = None,
    dist: int = None,
    local_authority: str = None,
    exemption_code: str = None,
) -> str:
    """Searches DEFRA environment API waste exemptions registry"""
    try:
        url = f"{__BASE_URL}/waste-exemptions/registration.json"
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
        if exemption_code:
            params["exemptionCode"] = exemption_code
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
            }

            # Handle holder (can be single object or array) - and has different structure with hasAddress
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
                        # Handle holder address
                        if holder.get("hasAddress", None):
                            address = holder.get("hasAddress")
                            holder_info["hasAddress"] = {
                                "address": address.get("address", None),
                                "postcode": address.get("postcode", None),
                                "organizationName": address.get(
                                    "organization_name", None
                                ),
                                "streetAddress": address.get("street_address", None),
                                "locality": address.get("locality", None),
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
                    # Handle holder address
                    if holder.get("hasAddress", None):
                        address = holder.get("hasAddress")
                        item_info["holder"]["hasAddress"] = {
                            "address": address.get("address", None),
                            "postcode": address.get("postcode", None),
                            "organizationName": address.get("organization_name", None),
                            "streetAddress": address.get("street_address", None),
                            "locality": address.get("locality", None),
                        }

            # Handle exemptions array
            if item.get("exemption", None):
                item_info["exemption"] = []
                for exemption in item.get("exemption"):
                    exemption_info = {
                        "id": exemption.get("@id", None),
                        "registrationDate": exemption.get("registrationDate", None),
                        "expiryDate": exemption.get("expiryDate", None),
                    }

                    # Handle registration type
                    if exemption.get("registrationType", None):
                        reg_type = exemption.get("registrationType")
                        exemption_info["registrationType"] = {
                            "id": reg_type.get("@id", None),
                            "prefLabel": reg_type.get("prefLabel", None),
                        }

                    # Handle code category
                    if exemption.get("codeCategory", None):
                        code_cat = exemption.get("codeCategory")
                        exemption_info["codeCategory"] = {
                            "id": code_cat.get("@id", None),
                            "notation": code_cat.get("notation", None),
                            "prefLabel": code_cat.get("prefLabel", None),
                        }

                        # Handle members array
                        if code_cat.get("member", None):
                            exemption_info["codeCategory"]["member"] = []
                            for member in code_cat.get("member"):
                                if isinstance(member, str):
                                    exemption_info["codeCategory"]["member"].append(
                                        member
                                    )
                                elif isinstance(member, dict):
                                    member_info = {
                                        "id": member.get("@id", None),
                                        "notation": member.get("notation", None),
                                        "description": member.get("description", None),
                                    }
                                    # Handle seeAlso
                                    if member.get("seeAlso", None):
                                        see_also = member.get("seeAlso")
                                        if isinstance(see_also, str):
                                            member_info["seeAlso"] = see_also
                                        elif isinstance(see_also, dict):
                                            member_info["seeAlso"] = {
                                                "id": see_also.get("@id", None),
                                            }
                                    exemption_info["codeCategory"]["member"].append(
                                        member_info
                                    )

                    item_info["exemption"].append(exemption_info)

            # Handle site array
            if item.get("site", None):
                item_info["site"] = []
                for site in item.get("site"):
                    site_info = {
                        "id": site.get("@id", None),
                        "distance": site.get("distance", None),
                    }

                    # Handle site address
                    if site.get("siteAddress", None):
                        address = site.get("siteAddress")
                        site_info["siteAddress"] = {
                            "address": address.get("address", None),
                            "postcode": address.get("postcode", None),
                            "organizationName": address.get("organization_name", None),
                            "streetAddress": address.get("street_address", None),
                            "locality": address.get("locality", None),
                            "postcodeURI": address.get("postcodeURI", None),
                        }

                    item_info["site"].append(site_info)

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"


def search_for_waste_exemption(
    id: str,
) -> str:
    """Searches DEFRA environment API waste exemptions registry for a particular registration"""
    try:
        url = f"{__BASE_URL}/waste-exemptions/registration/{id}.json"
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
            }

            # Handle holder (can be single object or array) - and has different structure with hasAddress
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
                        # Handle holder address
                        if holder.get("hasAddress", None):
                            address = holder.get("hasAddress")
                            holder_info["hasAddress"] = {
                                "address": address.get("address", None),
                                "postcode": address.get("postcode", None),
                                "organizationName": address.get(
                                    "organization_name", None
                                ),
                                "streetAddress": address.get("street_address", None),
                                "locality": address.get("locality", None),
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
                    # Handle holder address
                    if holder.get("hasAddress", None):
                        address = holder.get("hasAddress")
                        item_info["holder"]["hasAddress"] = {
                            "address": address.get("address", None),
                            "postcode": address.get("postcode", None),
                            "organizationName": address.get("organization_name", None),
                            "streetAddress": address.get("street_address", None),
                            "locality": address.get("locality", None),
                        }

            # Handle exemptions array
            if item.get("exemption", None):
                item_info["exemption"] = []
                for exemption in item.get("exemption"):
                    exemption_info = {
                        "id": exemption.get("@id", None),
                        "registrationDate": exemption.get("registrationDate", None),
                        "expiryDate": exemption.get("expiryDate", None),
                    }

                    # Handle registration type
                    if exemption.get("registrationType", None):
                        reg_type = exemption.get("registrationType")
                        exemption_info["registrationType"] = {
                            "id": reg_type.get("@id", None),
                            "prefLabel": reg_type.get("prefLabel", None),
                        }

                    # Handle code category
                    if exemption.get("codeCategory", None):
                        code_cat = exemption.get("codeCategory")
                        exemption_info["codeCategory"] = {
                            "id": code_cat.get("@id", None),
                            "notation": code_cat.get("notation", None),
                            "prefLabel": code_cat.get("prefLabel", None),
                        }

                        # Handle members array
                        if code_cat.get("member", None):
                            exemption_info["codeCategory"]["member"] = []
                            for member in code_cat.get("member"):
                                if isinstance(member, str):
                                    exemption_info["codeCategory"]["member"].append(
                                        member
                                    )
                                elif isinstance(member, dict):
                                    member_info = {
                                        "id": member.get("@id", None),
                                        "notation": member.get("notation", None),
                                        "description": member.get("description", None),
                                    }
                                    # Handle seeAlso
                                    if member.get("seeAlso", None):
                                        see_also = member.get("seeAlso")
                                        if isinstance(see_also, str):
                                            member_info["seeAlso"] = see_also
                                        elif isinstance(see_also, dict):
                                            member_info["seeAlso"] = {
                                                "id": see_also.get("@id", None),
                                            }
                                    exemption_info["codeCategory"]["member"].append(
                                        member_info
                                    )

                    item_info["exemption"].append(exemption_info)

            # Handle site array
            if item.get("site", None):
                item_info["site"] = []
                for site in item.get("site"):
                    site_info = {
                        "id": site.get("@id", None),
                        "distance": site.get("distance", None),
                    }

                    # Handle site address
                    if site.get("siteAddress", None):
                        address = site.get("siteAddress")
                        site_info["siteAddress"] = {
                            "address": address.get("address", None),
                            "postcode": address.get("postcode", None),
                            "organizationName": address.get("organization_name", None),
                            "streetAddress": address.get("street_address", None),
                            "locality": address.get("locality", None),
                            "postcodeURI": address.get("postcodeURI", None),
                        }

                    item_info["site"].append(site_info)

            items.append({item["@id"]: item_info})

        return json.dumps(items, indent=2)

    except Exception as e:
        return f"Error getting results from defra: {str(e)}"
