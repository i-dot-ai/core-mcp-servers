data "archive_file" "mcp" {
  type        = "zip"
  source_dir  = "${path.module}/../../../build/${var.source_name}"
  output_path = "${path.module}/../../../out/${var.source_name}.zip"
}

data "archive_file" "mcp_layer" {
  type        = "zip"
  source_dir  = "${path.module}/../../../build/packages/${var.source_name}"
  output_path = "${path.module}/../../../build/layers/${var.source_name}.zip"
}

resource "aws_lambda_layer_version" "mcp_dependencies" {
  filename         = data.archive_file.mcp_layer.output_path
  layer_name       = "${var.function_name}-layer"
  description      = "Dependency layer for ${var.function_name}"
  source_code_hash = data.archive_file.mcp_layer.output_base64sha256

  compatible_runtimes = [var.runtime]
  compatible_architectures = ["x86_64"]
}

module "mcp" {
  source = "git::https://github.com/i-dot-ai/i-dot-ai-core-terraform-modules.git//modules/infrastructure/lambda?ref=v2.1.0-lambda"
  # source = "../../../../i-dot-ai-core-terraform-modules//modules/infrastructure/lambda"  # For testing local changes
  function_name = var.function_name
  account_id    = var.account_id

  runtime          = var.runtime
  package_type     = "Zip"
  handler          = var.entrypoint
  file_path        = data.archive_file.mcp.output_path
  source_code_hash = data.archive_file.mcp.output_base64sha256
  layers = [aws_lambda_layer_version.mcp_dependencies.arn]

  timeout     = 60
  memory_size = var.memory_size

  environment_variables = {
    "REPO" : "core-mcp-servers",
    "ENVIRONMENT" : terraform.workspace,
  }
}
