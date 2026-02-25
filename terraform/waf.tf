module "waf" {
  # checkov:skip=CKV_TF_1: We're using semantic versions instead of commit hash
  # source                       = "../../i-dot-ai-core-terraform-modules//modules/infrastructure/waf"
  # For testing local changes
  source = "git::https://github.com/i-dot-ai/i-dot-ai-core-terraform-modules.git//modules/infrastructure/waf?ref=v7.2.0-waf"
  name                         = local.name
  host                         = "${module.api-gateway.rest_api.id}.execute-api.${data.aws_region.current.region}.amazonaws.com"
  env                          = var.env
  block_non_host_header_access = true

  header_secured_access_configuration = {
    kms_key_id = data.terraform_remote_state.platform.outputs.kms_key_arn
    hostname   = "${module.api-gateway.rest_api.id}.execute-api.${data.aws_region.current.region}.amazonaws.com"
    client_configs = [
      {
        client_name = var.project_name,
      },
    ]
  }
}

resource "aws_wafv2_web_acl_association" "api_gateway_waf" {
  resource_arn = module.api-gateway.rest_api_stage[0].arn
  web_acl_arn  = module.waf.web_acl_arn
}
