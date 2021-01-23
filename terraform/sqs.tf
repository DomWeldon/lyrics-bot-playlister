resource "aws_sqs_queue" "tweets" {
  name                        = "${var.project_name}-${var.environment_name}-tweets"
  fifo_queue                  = false
  content_based_deduplication = false
  visibility_timeout_seconds  = 60 * 60 * 12
}

resource "aws_lambda_event_source_mapping" "tweets" {
  batch_size       = 1
  event_source_arn = aws_sqs_queue.tweets.arn
  enabled          = true
  function_name    = module.tweet_lambda.lambda_arn
}

resource "aws_lambda_permission" "allows_sqs_to_trigger_lambda" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = module.tweet_lambda.lambda_name
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.tweets.arn
}
