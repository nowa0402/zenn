import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


class NotFound(BaseModel):
    msg: str = Field(...)


@app.get("/hello")
def hello_world() -> dict[str, str]:
    return {"hello": "world"}


# # 404エラーを拾う
# @app.exception_handler(404)
# def not_found(req: Request, exc: HTTPException) -> JSONResponse:
#     return JSONResponse(content={"notFound": str(req.url)}, status_code=404)


# contentは変換できれば何でもOK
# @app.exception_handler(404)
# def not_found(req: Request, exc: HTTPException) -> JSONResponse:
#     return JSONResponse(content=["abc", "def"], status_code=404)


# contentは変換できれば何でもOK
# @app.exception_handler(404)
# def not_found(req: Request, exc: HTTPException) -> JSONResponse:
#     return JSONResponse(content="sample", status_code=404)


# これはNG
# @app.exception_handler(404)
# def not_found_ng(req: Request, exc: HTTPException) -> JSONResponse:
#     return JSONResponse(content=NotFound(msg=str(req.url)), status_code=404)


# これはOK
@app.exception_handler(404)
def not_found_ok(req: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(content=NotFound(msg=str(req.url)).dict(), status_code=404)


# # ステータスコード変更
# @app.exception_handler(404)
# def not_found(req: Request, exc: HTTPException) -> JSONResponse:
#     return JSONResponse(content={"notFound": str(req.url)}, status_code=400)


def main() -> None:
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)


if __name__ == "__main__":
    main()
