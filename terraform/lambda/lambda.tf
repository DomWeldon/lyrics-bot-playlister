# actual lambda function
resource "aws_lambda_function" "this" {
  description = var.fn_description
  role        = aws_iam_role.execution.arn
  runtime     = var.runtime

  s3_bucket = aws_s3_bucket.lambda_source.id
  s3_key    = var.lambda_source_key

  function_name = local.fn_name
  handler       = var.fn_handler

  timeout     = var.fn_timeout
  memory_size = var.fn_memory_size
  publish     = true

  depends_on = [
    aws_s3_bucket_object.template
  ]

  dynamic "environment" {
    for_each = var.environment_variables
    content {
      variables = environment.value
    }
  }

  tags = local.tags
}
