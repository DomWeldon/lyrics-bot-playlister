import os
import typing

import fastapi
import mangum
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .. import config
from . import twitter

app = fastapi.FastAPI(root_path=config.api.ROOT_PATH)

# register sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN is not None and len(SENTRY_DSN):
    sentry_sdk.init(dsn=SENTRY_DSN)
    # logging.info("added Sentry", dsn=settings.SENTRY_DSN)
    app.add_middleware(SentryAsgiMiddleware)

# register twitter router
app.include_router(
    twitter.router,
    prefix="/webhook/twitter",
    tags=["Twitter 🐦 Endpoints"],
)


@app.get("/")
def read_root() -> typing.Dict[str, typing.List[str]]:
    return {"I dreamed about you for": ["Year"] * 29}


@app.get("/error")
def mock_error() -> None:
    # explain everything to the geeks in Sentry
    raise Exception(
        """
    Man, it's all been forgiven
    The swans are a-swimmin'
    I'll explain everything to the geeks
    """
    )


handler = mangum.Mangum(app, lifespan="auto")
