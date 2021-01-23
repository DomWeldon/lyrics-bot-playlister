
# the policy for the CI role
data "aws_iam_policy_document" "lambda_lyrics_s3" {

  # allow CI role to upload to lambda buckets for all three functions
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:HeadObject",
    ]

    resources = [
      aws_s3_bucket.lyrics.arn,
      "${aws_s3_bucket.lyrics.arn}/${aws_s3_bucket_object.lyrics.id}",
    ]
  }
}

# policy onto the role
resource "aws_iam_role_policy" "lambda_lyrics_s3" {
  name   = "${var.project_name}--${var.environment_name}-tweet-query-lambda-lyrics-s3"
  role   = module.tweet_query_lambda.lambda_execution_role_id
  policy = data.aws_iam_policy_document.lambda_lyrics_s3.json
}
