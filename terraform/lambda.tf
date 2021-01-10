module "fastapi_asgi_lambda" {
  source           = "./lambda"
  project_name     = var.project_name
  environment_name = var.environment_name
  fn_name          = var.asgi_fn_name
  fn_handler       = var.asgi_fn_handler

  environment_variables = [{
    # project
    ENV              = var.environment_name
    PROJECT_NAME     = var.project_name
    ENVIRONMENT_NAME = var.environment_name
    # sentry
    SENTRY_DSN = sentry_key.asgi.dsn_public
    # twitter
    TWITTER_CONSUMER_KEY        = var.twitter_consumer_key
    TWITTER_CONSUMER_KEY_SECRET = var.twitter_consumer_key_secret
    TWITTER_ACCESS_TOKEN        = var.twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET = var.twitter_access_token_secret
  }]
}
