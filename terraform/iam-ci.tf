# continious integration user
resource "aws_iam_user" "ci" {
  name = "ci"
  path = "/${replace(var.project_name, "-", "")}/${replace(var.environment_name, "-", "")}/deployment/"

  tags = local.tags
}

# key to use for auth
resource "aws_iam_access_key" "ci" {
  user = aws_iam_user.ci.name
}

# allow the CI user to assume a role
data "aws_iam_policy_document" "ci_sts" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "AWS"

      identifiers = [aws_iam_user.ci.arn]
    }
  }
}

# allow the CI use to assume role by creating assume_role_policy
resource "aws_iam_role" "ci" {
  name               = "${var.project_name}--${var.environment_name}-ci"
  assume_role_policy = data.aws_iam_policy_document.ci_sts.json

  tags = local.tags
}

# the policy for the CI role
data "aws_iam_policy_document" "ci" {

  # allow CI role to upload to lambda buckets for all three functions
  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:GetObjectVersion",
    ]

    resources = [
      module.fastapi_asgi_lambda.source_bucket_arn,
      "${module.fastapi_asgi_lambda.source_bucket_arn}/*",
      module.tweet_query_lambda.source_bucket_arn,
      "${module.tweet_query_lambda.source_bucket_arn}/*",
      module.tweet_lambda.source_bucket_arn,
      "${module.tweet_lambda.source_bucket_arn}/*",
    ]
  }

  # allow CI role to update all three function codes
  statement {
    effect = "Allow"

    actions = [
      "lambda:UpdateFunctionCode"
    ]

    resources = [
      module.fastapi_asgi_lambda.lambda_arn,
      "${module.fastapi_asgi_lambda.lambda_arn}/*",
      module.tweet_query_lambda.lambda_arn,
      "${module.tweet_query_lambda.lambda_arn}/*",
      module.tweet_lambda.lambda_arn,
      "${module.tweet_lambda.lambda_arn}/*",
    ]
  }

  # allow to get all SSM parameters
  statement {
    effect = "Allow"

    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters"
    ]

    resources = [
      # asgi
      aws_ssm_parameter.asgi_lambda_arn.arn,
      aws_ssm_parameter.asgi_source_bucket_id.arn,
      aws_ssm_parameter.asgi_source_key.arn,
      # tweet query
      aws_ssm_parameter.tweet_query_lambda_arn.arn,
      aws_ssm_parameter.tweet_query_source_bucket_id.arn,
      aws_ssm_parameter.tweet_query_source_key.arn,
      # tweet
      aws_ssm_parameter.tweet_lambda_arn.arn,
      aws_ssm_parameter.tweet_source_bucket_id.arn,
      aws_ssm_parameter.tweet_source_key.arn,
    ]
  }
}

# policy onto the role
resource "aws_iam_role_policy" "ci" {
  name   = "${var.project_name}--${var.environment_name}-ci"
  role   = aws_iam_role.ci.id
  policy = data.aws_iam_policy_document.ci.json
}
