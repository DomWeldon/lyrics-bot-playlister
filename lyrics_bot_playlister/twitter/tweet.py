"""Consume the queue and tweet out song names."""
import os

import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# from .. import config
# from . import api

# register sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN is not None and len(SENTRY_DSN):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[AwsLambdaIntegration()],
    )


def handler(event, context):
    print(event, context)
