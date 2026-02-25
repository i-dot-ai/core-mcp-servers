data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_wafv2_ip_set" "ip_whitelist_internal" {
  name  = "i-dot-ai-core-ip-config-ip-set-internal"
  scope = var.scope
}

data "terraform_remote_state" "core-auth" {
  backend   = "s3"
  workspace = terraform.workspace
  config = {
    bucket = var.state_bucket
    key    = "core-auth-api/terraform.tfstate"
    region = var.region
  }
}

data "terraform_remote_state" "platform" {
  backend   = "s3"
  workspace = terraform.workspace
  config = {
    bucket = var.state_bucket
    key    = "platform/terraform.tfstate"
    region = var.region
  }
}

data "aws_route53_zone" "zone" {
  name = local.is_production ? var.domain_name : "${terraform.workspace}.${var.domain_name}"
}

locals {
  root_domain_name = "i.ai.gov.uk"
  host_name = local.is_production ? "core-mcp-servers.${local.root_domain_name}" : "core-mcp-servers.${terraform.workspace}.${local.root_domain_name}"
}
