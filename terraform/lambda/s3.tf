# local file for first deploy
data "local_file" "template" {
  filename = "${path.module}/src/main.py"
}

resource "local_file" "template" {
  content  = data.local_file.template.content
  filename = "${path.module}/.artefact/main.py"
}

data "archive_file" "template" {
  depends_on = [
    local_file.template,
  ]

  type        = "zip"
  output_path = "${path.module}/.artefact.zip"
  source_dir  = "${path.module}/.artefact"
}

# bucket to store it in
resource "aws_s3_bucket" "lambda_source" {
  bucket = local.lambda_source_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  tags   = local.tags
}

resource "aws_s3_bucket_public_access_block" "lambda_source" {
  bucket = aws_s3_bucket.lambda_source.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}

# store the file in the bucket
resource "aws_s3_bucket_object" "template" {
  depends_on = [
    data.archive_file.template
  ]

  bucket = aws_s3_bucket.lambda_source.id
  key    = var.lambda_source_key
  source = "${path.module}/.artefact.zip"
}
