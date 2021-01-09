locals {
  lambda_source_bucket_name = var.lambda_source_bucket_name != "" ? var.lambda_source_bucket_name : "${var.project_name}--${var.environment_name}--${var.fn_name}--source"
  tags = var.tags != {} ? var.tags : {
    Project      = var.project_name,
    Environment  = var.environment_name,
    FunctionName = var.fn_name,
  }
  fn_name = var.fn_name != "" ? var.fn_name : "${var.project_name}--${var.environment_name}--${var.fn_name}"
}
