
resource "aws_s3_bucket" "lyrics" {
  bucket = var.lyrics_s3_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = local.tags
}

resource "aws_s3_bucket_public_access_block" "lyrics" {
  bucket = aws_s3_bucket.lyrics.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket_object" "lyrics" {
  bucket = aws_s3_bucket.lyrics.id
  key    = var.lyrics_s3_key
  source = var.lyrics_file_path
  etag   = filemd5(var.lyrics_file_path)
}
