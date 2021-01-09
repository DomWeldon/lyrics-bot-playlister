resource "circleci_project" "main" {
  name = var.circleci_project_name
}

resource "circleci_environment_variable" "aws_access_key_id" {
  project = circleci_project.main.id
  name    = "AWS_ACCESS_KEY_ID"
  value   = aws_iam_access_key.ci.id
}

resource "circleci_environment_variable" "aws_secret_access_key" {
  project = circleci_project.main.id
  name    = "AWS_SECRET_ACCESS_KEY"
  value   = aws_iam_access_key.ci.secret
}

resource "circleci_environment_variable" "aws_role_arn" {
  project = circleci_project.main.id
  name    = "AWS_ROLE_ARN_${var.environment_name}"
  value   = aws_iam_role.ci.arn
}
