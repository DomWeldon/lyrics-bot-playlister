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

// twitter
# locals {
#   twitter_secrets = {
#     twitter_consumer_key        = var.twitter_consumer_key
#     twitter_consumer_key_secret = var.twitter_consumer_key_secret
#     twitter_access_token        = var.twitter_access_token
#     twitter_access_token_secret = var.twitter_access_token_secret
#   }
# }
#
# resource "aws_ssm_parameter" "twitter_secret" {
#   for_each = local.twitter_secrets
#
#   name      = "/${var.project_name}/${var.environment_name}/twitter/${replace(each.key, "twitter", "")}"
#   type      = "SecureString"
#   value     = each.value
#   overwrite = true
#   tags      = local.tags
# }
