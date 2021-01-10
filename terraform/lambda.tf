module "fastapi_asgi_lambda" {
  source           = "./lambda"
  project_name     = var.project_name
  environment_name = var.environment_name
  fn_name          = var.asgi_fn_name
  fn_handler       = var.asgi_fn_handler

  environment_variables = [{
    ENV              = var.environment_name
    PROJECT_NAME     = var.project_name
    ENVIRONMENT_NAME = var.environment_name
    SENTRY_DSN       = sentry_key.asgi.dsn_public
  }]
}
