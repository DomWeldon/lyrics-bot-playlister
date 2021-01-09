# mostly for namespacing
variable "project_name" {
  default     = ""
  description = "name of project for namespacing"
  type        = string
}

variable "environment_name" {
  default     = "Dev"
  type        = string
  description = "Prod/Staging/Dev etc."
}

# function environment / code
variable "environment_variables" {
  default     = []
  type        = list(any)
  description = "Environment variables passed to the function."
}

variable "runtime" {
  default     = "python3.8"
  type        = string
  description = "Runtime environment"
}

# CI pipelining
variable "lambda_source_bucket_name" {
  default     = ""
  type        = string
  description = "Name of bucket to store the function source in."
}

variable "lambda_source_key" {
  default     = "artefact.zip"
  type        = string
  description = "Name of bucket to store the function source in."
}

variable "ssm_parameter_arns" {
  default     = []
  type        = list(string)
  description = "List of SSM ARNs the function needs to access"
}

# function related
variable "fn_handler" {
  default     = "main.main"
  type        = string
  description = "Entrypoint/handler for the lambda"
}

variable "fn_memory_size" {
  default     = 1024
  type        = number
  description = "Function memory size"
}

variable "fn_timeout" {
  type        = number
  default     = 5
  description = "Timeout in seconds"
}

variable "fn_name" {
  type        = string
  description = "Function name"
}

variable "fn_description" {
  default     = "Lambda function managed by Terraform"
  type        = string
  description = "Description to attach to the lambda function"
}

variable "tags" {
  default     = {}
  description = "Tags for every resource"
  type        = map(any)
}
