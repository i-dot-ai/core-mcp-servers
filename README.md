# core-mcp-servers

This repository manages the deployment of MCP servers that don't logically fit within any particular repo.

Each MCP server is deployed as a separate lambda, with API gateway acting as the ingress to them.

## Important links

### API gateway ingress URLs
[Dev gateway](https://core-mcp-servers.dev.i.ai.gov.uk/)
<br>[Preprod gateway](https://core-mcp-servers.i.ai.gov.uk/)
<br>[Prod gateway](https://core-mcp-servers.i.ai.gov.uk/)

### Available MCP servers

#### Civil Service Acronyms MCP Server

An MCP server for searching the [Civil Service Acronym Buster](https://acronyms.toolsforcivilservants.co.uk)

More information on the website can be found at the [Civil Service Acronym Buster github repo](https://github.com/Samuel-Hoskin/CS-Acronyms)

#### Gov.uk Search MCP Server

An MCP for searching the [Gov UK search API](https://github.com/alphagov/search-api) for general information from govuk pages.

This provides an up-to-date reference for LLMs to work with when specifically querying for content on [gov.uk](https://gov.uk).

#### Wikipedia MCP Server

An MCP server for searching Wikipedia and retrieving article content and summaries.

Provides tools to search for pages, get full page content, and summarize topics from Wikipedia.

#### DEFRA Environment API MCP Server

An MCP server for accessing the [DEFRA Environment Agency Public Register](https://environment.data.gov.uk/public-register).

This server provides comprehensive access to UK environmental data across 11 registries with 22 tools:

**General Registry Tools:**
- `search_across_registries` - Search across all registries
- `simple_name_search` - Simple name/number search

**Waste Operations:**
- `search_waste_operations` - Search waste operations registry
- `search_for_waste_operation` - Get specific waste operation by ID

**End of Life Vehicles:**
- `search_end_of_life_vehicles` - Search vehicle facilities registry
- `search_for_end_of_life_vehicle` - Get specific facility by ID

**Enforcement Actions:**
- `search_enforcement_action` - Search enforcement actions registry
- `search_for_enforcement_action` - Get specific enforcement action by ID

**Flood Risk Activity Exemptions:**
- `search_flood_risk_exemptions` - Search flood risk exemptions registry
- `search_for_flood_risk_exemption` - Get specific exemption by ID

**Industrial Installations:**
- `search_industrial_installations` - Search industrial installations registry
- `search_for_industrial_installation` - Get specific installation by ID

**Radioactive Substance Permits:**
- `search_radioactive_substance` - Search radioactive substance permits registry
- `search_for_radioactive_substance` - Get specific permit by ID

**Scrap Metal Dealers:**
- `search_scrap_metal_dealers` - Search scrap metal dealers registry
- `search_for_scrap_metal_dealer` - Get specific dealer by ID

**Waste Exemptions:**
- `search_waste_exemptions` - Search waste exemptions registry
- `search_for_waste_exemption` - Get specific exemption by ID

**Waste Carriers and Brokers:**
- `search_waste_carriers_brokers` - Search waste carriers/brokers registry
- `search_for_waste_carrier_broker` - Get specific carrier/broker by ID

**Water Discharges:**
- `search_water_discharges` - Search water discharge consents registry
- `search_for_water_discharge` - Get specific consent by ID

### Adding a new MCP server

> [!WARNING]  
> Lambda has a maximum unzipped size of 250mb total (code and packages layers), so please keep them short and sweet.
> If you need more space, please raise this as a new feature request to support containerised MCPs.

Currently, we only support python as an option as getting this to work initially was somewhat convoluted and against spec.

However, we would like to also enable JS lambdas in the future and have that as an option.

To add a new server, the following steps need to be taken:

1. Add another dir to `src/` with the name matching the mcp server and lambda you want to deploy
2. Add your code into `main.py` inside the `src/<your_lambda_name>/code/` dir
   1. Use on of the existing lambdas as an example
3. Add required packages into `requirements.txt` inside the `src/<your_lambda_name>/code/` dir
4. Add the deployment and lint steps to the `Makefile` inside the `src/<your_lambda_name>/` dir
5. Add your lambda information to `terraform/spec/mcpservers-oas30.yaml` file (copy one of the existing ones and just change the references)
6. Add your lambda config as a module call to `terraform/lambdas.tf` file
7. Update the list of MCP servers to build in the root `Makefile`, in `build_artifacts` and `lint` commands

> [!TIP]
> There are examples in the above terraform files for the terraform steps. And `src/gov_uk_acronyms/` for the python part.


## Deploying

Deployments will happen automatically when merging to `main` for `prod` or when creating a manual `release` for `dev`.

To deploy manually using terraform, run `make build_artifacts` to create the build scripts, 
and `export env=<env>`+`make tf_apply` to deploy.

## Security

The api gateway is publicly available on the internet from a network perspective, and has a two layer defence setup. 

1. The domain access policy is configured to block all traffic except from known Cabinet Office/DSIT IP addresses.
   1. As this is currently aimed to host tools that are stateless, and use public sources or produce public information,
   blocking that requires more than this is too restrictive for the time being
   2. Accessing the MCP requires you to know the value of the WAF header token

The intention is to eventually place this behind an auth mechanism of some kind that matches the MCP spec, if and when the hosted tools demand it.
