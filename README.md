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

### Adding a new MCP server

> [!WARNING]  
> Lambda has a maximum unzipped size of 250mb total (code and packages layers), so please keep them short and sweet.
> If you need more space, please raise this as a new feature request to support containerised MCPs.

Currently, we only support python as an option as getting this to work initially was somewhat convoluted and against spec.

However, we would like to also enable JS lambdas in the future and have that as an option.

To add a new server, the following steps need to be taken:

1. Add another dir to `src/` with the name matching the mcp server and lambda you want to deploy
2. Add your code into `tools.py` inside the `src/<your_lambda_name>/code/` dir
3. Add required packages into `requirements.txt` inside the `src/<your_lambda_name>/code/` dir
4. Add the deployment and lint steps to the `Makefile` inside the `src/<your_lambda_name>/` dir
5. Add your lambda information to `terraform/api_gateway.tf` `local.mcp_servers` variable
6. Add your lambda config as a module call to `terraform/lambdas.tf` file
7. Update the list of MCP servers to build in the root `Makefile`, in `build_artifacts/ci` and `lint` commands

> [!TIP]
> There are examples in the above terraform files for the terraform steps. And `src/gov_uk_acronyms/` for the python part.


## Deploying

Deployments will happen automatically when merging to `main` for `prod` or when creating a manual `release` for `dev`.

To deploy manually using terraform, run `make build_artifacts/ci` to create the build scripts, 
and `export env=<env>`+`make tf_apply` to deploy.

## Security

The api gateway is publicly available on the internet from a network perspective, and has a single layer defence setup. 

1. The domain access policy is configured to block all traffic except from known Cabinet Office/DSIT IP addresses.
   2. As this is currently aimed to host tools that are stateless, and use public sources or produce public information,
   blocking that requires more than this is too restrictive for the time being

The intention is to eventually place this behind a keycloak instance (or another auth service) if and when the hosted tools demand it.
