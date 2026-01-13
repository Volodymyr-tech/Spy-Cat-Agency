import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import TokenExpiredException, TokenNoFoundException
from app.user.router import router as users_router
static_dir = os.path.join(os.path.dirname(__file__), "static")


app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=settings.run.host, port=settings.run.port)