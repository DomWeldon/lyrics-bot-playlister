locals {
  tags = var.tags != {} ? var.tags : {
    Project     = var.project_name,
    Environment = var.environment_name,
  }
}
