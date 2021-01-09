data "aws_iam_policy_document" "sts" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"

      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

data "aws_iam_policy" "lambda_vpc_access" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

data "aws_iam_policy_document" "execution" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
      "logs:GetLogEvents",
      "logs:FilterLogEvents",
    ]

    resources = [
      "arn:aws:logs:*:*:*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "lambda:GetFunction",
    ]

    resources = [
      aws_lambda_function.this.arn,
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
    ]

    resources = [
      aws_s3_bucket.lambda_source.arn,
      "${aws_s3_bucket.lambda_source.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.execution.name
  policy_arn = data.aws_iam_policy.lambda_vpc_access.arn
}

resource "aws_iam_role_policy" "execution" {
  name   = "${local.fn_name}-execution"
  role   = aws_iam_role.execution.id
  policy = data.aws_iam_policy_document.execution.json
}

resource "aws_iam_role" "execution" {
  name               = "${var.project_name}-${var.fn_name}-execution"
  assume_role_policy = data.aws_iam_policy_document.sts.json

  tags = local.tags
}
