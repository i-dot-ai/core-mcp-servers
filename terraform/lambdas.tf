locals {
  mcp_servers = {
    "gov_uk_search" = {
      function_name = module.gov_uk_search.name
      invoke_arn    = module.gov_uk_search.invokation_arn
      arn           = module.gov_uk_search.arn
    },
    "gov_uk_acronyms" = {
      function_name = module.gov_uk_acronyms.name
      invoke_arn    = module.gov_uk_acronyms.invokation_arn
      arn           = module.gov_uk_acronyms.arn
    },
    "wikipedia" = {
      function_name = module.wikipedia.name
      invoke_arn    = module.wikipedia.invokation_arn
      arn           = module.wikipedia.arn
    }
  }
}

module "gov_uk_search" {
  source = "./modules/mcp-server-lambda"
  source_name = "gov_uk_search"
  function_name = "${local.name}-gov-uk-search"
  runtime = "python3.12"
  account_id = data.aws_caller_identity.current.account_id
  entrypoint = "main.lambda_handler"
}

module "gov_uk_acronyms" {
  source = "./modules/mcp-server-lambda"
  source_name = "gov_uk_acronyms"
  function_name = "${local.name}-gov-uk-acronyms"
  runtime = "python3.12"
  account_id = data.aws_caller_identity.current.account_id
  entrypoint = "main.lambda_handler"
}

module "wikipedia" {
  source = "./modules/mcp-server-lambda"
  source_name = "wikipedia"
  function_name = "${local.name}-wikipedia"
  runtime = "python3.12"
  account_id = data.aws_caller_identity.current.account_id
  entrypoint = "main.lambda_handler"
}
