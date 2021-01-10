variable "project_name" {
  type        = string
  description = "Name of the project"
}

variable "environment_name" {
  type        = string
  description = "Name of the environment"
}

variable "asgi_fn_handler" {
  type        = string
  description = "Handler for the ASGI lambda function"
}

variable "asgi_fn_name" {
  type        = string
  description = "Name for the ASGI lambda function"
}

variable "tags" {
  default = {}
}

variable "aws_region" {
  default = "eu-west-1"
}


# circleci
variable "circleci_project_name" {
  type        = string
  description = "Repository name in CircleCI"
}

variable "circleci_vcs_type" {
  type        = string
  description = "e.g. GitHub"
}

variable "circleci_organization" {
  type        = string
  description = "For VCS Type"
}


# sentry
variable "sentry_organization" {
  type        = string
  description = "Sentry org name"
}

variable "sentry_organization_slug" {
  type        = string
  description = "Sentry org slug"
}

variable "sentry_team" {
  type        = string
  description = "Sentry team name"
}

variable "sentry_team_slug" {
  type        = string
  description = "Sentry team slug"
}

# twitter
variable "twitter_consumer_key" {
  type = string
}
variable "twitter_consumer_key_secret" {
  type = string
}
variable "twitter_access_token" {
  type = string
}
variable "twitter_access_token_secret" {
  type = string
}
