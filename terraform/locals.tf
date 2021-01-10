locals {
  tags = var.tags != {} ? var.tags : {
    Project     = var.project_name,
    Environment = var.environment_name,
  }

  api_gateway_name = "/${var.project_name}/${var.environment_name}/main"
}
