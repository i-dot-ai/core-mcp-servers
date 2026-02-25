locals {
  mcp_server_arns = {
    for key, server in local.mcp_servers : key => server.arn
  }
  lambda_arns = merge(
    local.mcp_server_arns,
    {
      "healthcheck" = "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:i-dot-ai-dev-core-auth-api-healthcheck"
    }
  )
}

module "api-gateway" {
  # checkov:skip=CKV_TF_1: We're using semantic versions instead of commit hash
  # source = "../../i-dot-ai-core-terraform-modules//modules/infrastructure/api-gateway" # For testing local changes
  source = "git::https://github.com/i-dot-ai/i-dot-ai-core-terraform-modules.git//modules/infrastructure/api-gateway?ref=v1.1.0-api-gateway"

  allowed_origin = "*"
  api_name       = "${local.name}-module"
  lambda_arns    = local.lambda_arns
  private_api    = false
  templatefile   = "spec/mcpservers-oas30.yaml"
  stages = [
    {
      name                  = "core-mcp-servers"
      description           = "This is the deployment for the ${var.env} auth api"
      metrics_enabled       = false
      logging_level         = null
      log_retention         = 7
      caching_enabled       = false,
      cache_cluster_enabled = false,
      cache_cluster_size    = "0.5",
      xray_tracing_enabled  = false

    }
  ]
}

resource "aws_lambda_permission" "lambda_permission_post" {
  for_each = local.mcp_servers

  statement_id  = "AllowExecutionFromAPIGateway-POST-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${module.api-gateway.rest_api.execution_arn}/*/POST/${each.key}"
}

resource "aws_lambda_permission" "lambda_permission_options" {
  for_each = local.mcp_servers

  statement_id  = "AllowExecutionFromAPIGateway-OPTIONS-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${module.api-gateway.rest_api.execution_arn}/*/OPTIONS/${each.key}"
}
