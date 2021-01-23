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

// tweet query lambda
resource "aws_ssm_parameter" "tweet_query_lambda_arn" {
  name      = "/${var.project_name}/${var.environment_name}/tweet_query/lambda/arn"
  type      = "String"
  value     = module.tweet_query_lambda.lambda_arn
  overwrite = true
  tags      = local.tags
}

resource "aws_ssm_parameter" "tweet_query_source_bucket_id" {
  name      = "/${var.project_name}/${var.environment_name}/tweet_query/source/bucket_id"
  type      = "String"
  value     = module.tweet_query_lambda.source_bucket_id
  overwrite = true
  tags      = local.tags
}

resource "aws_ssm_parameter" "tweet_query_source_key" {
  name      = "/${var.project_name}/${var.environment_name}/tweet_query/source/key"
  type      = "String"
  value     = module.tweet_query_lambda.source_key
  overwrite = true
  tags      = local.tags
}

// tweet lambda
resource "aws_ssm_parameter" "tweet_lambda_arn" {
  name      = "/${var.project_name}/${var.environment_name}/tweet/lambda/arn"
  type      = "String"
  value     = module.tweet_lambda.lambda_arn
  overwrite = true
  tags      = local.tags
}

resource "aws_ssm_parameter" "tweet_source_bucket_id" {
  name      = "/${var.project_name}/${var.environment_name}/tweet/source/bucket_id"
  type      = "String"
  value     = module.tweet_lambda.source_bucket_id
  overwrite = true
  tags      = local.tags
}

resource "aws_ssm_parameter" "tweet_source_key" {
  name      = "/${var.project_name}/${var.environment_name}/tweet/source/key"
  type      = "String"
  value     = module.tweet_lambda.source_key
  overwrite = true
  tags      = local.tags
}
