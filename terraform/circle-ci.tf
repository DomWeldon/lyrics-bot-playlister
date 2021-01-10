resource "circleci_project" "main" {
  name = var.circleci_project_name
}

locals {
  ci_environment_vars = {
    AWS_ACCESS_KEY_ID                             = aws_iam_access_key.ci.id
    AWS_SECRET_ACCESS_KEY                         = aws_iam_access_key.ci.secret
    "AWS_ROLE_ARN_${upper(var.environment_name)}" = aws_iam_role.ci.arn
    PROJECT_NAME                                  = var.project_name
    AWS_REGION                                    = var.aws_region
  }
}

resource "circleci_environment_variable" "aws_access_key_id" {
  for_each = local.ci_environment_vars

  project = circleci_project.main.id
  name    = each.key
  value   = each.value
}
