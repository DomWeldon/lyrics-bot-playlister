terraform {
  backend "s3" {
    # configure this as needed
    bucket = "nationalbot-the-terraform-state"
    # this should be the environment name
    key     = "state"
    profile = "lyrics-bot-playlister"
    region  = "eu-west-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.21.0"
    }

    circleci = {
      source  = "tomtucka/circleci"
      version = "~> 0.4.0"
    }

    sentry = {
      source  = "jianyuan/sentry"
      version = "~> 0.6.0"
    }
  }
}
