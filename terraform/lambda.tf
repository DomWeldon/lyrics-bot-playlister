// lambda to power the API for responding to tweets
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
    API_ROOT_PATH    = "/${var.environment_name}"
    # API_INVOKE_BASE  = aws_api_gateway_stage.main.invoke_url
    # sentry
    SENTRY_DSN = sentry_key.asgi.dsn_public
    # twitter
    TWITTER_CONSUMER_KEY        = var.twitter_consumer_key
    TWITTER_CONSUMER_KEY_SECRET = var.twitter_consumer_key_secret
    TWITTER_ACCESS_TOKEN        = var.twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET = var.twitter_access_token_secret
  }]
}

// lambda to regularly query for the latest tweet
module "tweet_query_lambda" {
  source           = "./lambda"
  project_name     = var.project_name
  environment_name = var.environment_name
  fn_name          = var.tweet_query_fn_name
  fn_handler       = var.tweet_query_fn_handler

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
    # s3
    S3_LYRICS_BUCKET = aws_s3_bucket.lyrics.id
    S3_LYRICS_KEY    = var.lyrics_s3_key
    # sqs
    SQS_QUEUE_NAME  = aws_sqs_queue.tweets.name
    SQS_REGION_NAME = var.aws_region
  }]
}


module "tweet_lambda" {
  source           = "./lambda"
  project_name     = var.project_name
  environment_name = var.environment_name
  fn_name          = var.tweet_fn_name
  fn_handler       = var.tweet_fn_handler

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
