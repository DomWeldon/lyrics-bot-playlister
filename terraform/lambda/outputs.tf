
output "lambda_arn" {
  value = aws_lambda_function.this.arn
}

output "lambda_qualified_arn" {
  value = aws_lambda_function.this.qualified_arn
}

output "lambda_invoke_arn" {
  value = aws_lambda_function.this.invoke_arn
}

output "lambda_name" {
  value = local.fn_name
}

output "lambda_last_modified" {
  value = aws_lambda_function.this.last_modified
}

output "lambda_version" {
  value = aws_lambda_function.this.version
}

output "source_bucket_domain_name" {
  value = aws_s3_bucket.lambda_source.bucket_domain_name
}

output "source_bucket_arn" {
  value = aws_s3_bucket.lambda_source.arn
}

output "source_bucket_id" {
  value = aws_s3_bucket.lambda_source.id
}

output "source_key" {
  value = var.lambda_source_key
}

output "lambda_execution_role_id" {
  value = aws_iam_role.execution.id
}
