
resource "aws_cloudwatch_event_rule" "once_an_hour" {
  name                = "once-an-hour"
  description         = "Fires once an hour"
  schedule_expression = var.tweet_query_cron
}

resource "aws_cloudwatch_event_target" "bindicator" {
  rule      = aws_cloudwatch_event_rule.once_an_hour.name
  target_id = "lambda"
  arn       = module.tweet_query_lambda.lambda_arn
}

resource "aws_lambda_permission" "bindicator" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.tweet_query_lambda.lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.once_an_hour.arn
}
