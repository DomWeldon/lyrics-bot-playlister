import typing

import fastapi
import mangum

app = fastapi.FastAPI()


@app.get("/")
def read_root() -> typing.Dict[str, typing.List[str]]:
    return {"I dreamed about you for": ["Year"] * 29}


handler = mangum.Mangum(app)
