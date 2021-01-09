// app lambda
resource "aws_ssm_parameter" "asgi_lambda_arn" {
  name      = "/${var.project_name}/${var.environment_name}/asgi/lambda/arn"
  type      = "String"
  value     = module.fastapi_asgi_lambda.lambda_arn
  overwrite = true
  tags      = local.tags
}

resource "aws_ssm_parameter" "asgi_source_bucket_id" {
  name      = "/${var.project_name}/${var.environment_name}/asgi/source/bucket_id"
  type      = "String"
  value     = module.fastapi_asgi_lambda.source_bucket_id
  overwrite = true
  tags      = local.tags
}

resource "aws_ssm_parameter" "asgi_source_key" {
  name      = "/${var.project_name}/${var.environment_name}/asgi/source/key"
  type      = "String"
  value     = module.fastapi_asgi_lambda.source_key
  overwrite = true
  tags      = local.tags
}
