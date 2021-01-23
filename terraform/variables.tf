variable "project_name" {
  type        = string
  description = "Name of the project"
}

variable "environment_name" {
  type        = string
  description = "Name of the environment"
}

// lambda for powering the API to respond to tweets
variable "asgi_fn_handler" {
  type        = string
  description = "Handler for the ASGI lambda function"
}

variable "asgi_fn_name" {
  type        = string
  description = "Name for the ASGI lambda function"
}

// lambda to query for tweets
variable "tweet_query_fn_handler" {
  type        = string
  description = "Handler for the ASGI lambda function"
}

variable "tweet_query_fn_name" {
  type        = string
  description = "Name for the ASGI lambda function"
}

variable "tweet_query_cron" {
  type        = string
  description = "How frequently to query for new tweets"
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

// need to store the lyrics somewhere
variable "lyrics_s3_bucket_name" {
  type = string
}

variable "lyrics_s3_key" {
  default = "all-songs.yml"
  type    = string
}

variable "lyrics_file_path" {
  type = string
}
