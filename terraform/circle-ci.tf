resource "circleci_project" "main" {
  name = var.circleci_project_name
}

locals {
  ci_environment_vars = {
    # aws
    AWS_ACCESS_KEY_ID     = aws_iam_access_key.ci.id
    AWS_SECRET_ACCESS_KEY = aws_iam_access_key.ci.secret
    AWS_REGION            = var.aws_region
    # aws specific to branch
    "AWS_ROLE_ARN_${upper(var.environment_name)}" = aws_iam_role.ci.arn
    # preoject
    PROJECT_NAME = var.project_name
    # api
    API_INVOKE_BASE = aws_api_gateway_stage.main.invoke_url
    # twitter
    TWITTER_CONSUMER_KEY        = var.twitter_consumer_key
    TWITTER_CONSUMER_KEY_SECRET = var.twitter_consumer_key_secret
    TWITTER_ACCESS_TOKEN        = var.twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET = var.twitter_access_token_secret
  }
}

resource "circleci_environment_variable" "aws_access_key_id" {
  for_each = local.ci_environment_vars

  project = circleci_project.main.id
  name    = each.key
  value   = each.value
}
