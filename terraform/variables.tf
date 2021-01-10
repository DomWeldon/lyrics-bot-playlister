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
