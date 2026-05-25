import time

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.routes import router
from backend.core.config import get_settings
from backend.core.errors import AgroBuddyError
from backend.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = structlog.get_logger(__name__)

app = FastAPI(
    title="AgroBuddy API",
    description="AI-powered farmer assistance backend with crop disease prediction, chat, speech, and Telegram support.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round((time.perf_counter() - started) * 1000, 2),
    )
    return response


@app.exception_handler(AgroBuddyError)
async def agrobuddy_error_handler(_: Request, exc: AgroBuddyError) -> JSONResponse:
    logger.warning("application_error", error=exc.message)
    return JSONResponse(status_code=400, content={"detail": {"error": exc.message}})


@app.exception_handler(Exception)
async def generic_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_error", error=str(exc))
    return JSONResponse(status_code=500, content={"detail": {"error": "Internal server error"}})


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=settings.api_host, port=settings.api_port, reload=settings.app_env == "development")
