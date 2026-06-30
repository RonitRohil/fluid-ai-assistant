import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute

from app.config import GROQ_API_KEY
from app.api.v1.router import router as v1_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set in environment")
    routes = [
        f"  {', '.join(r.methods or [])} {r.path}"
        for r in app.routes
        if isinstance(r, APIRoute)
    ]
    logger.info("Registered routes:\n%s", "\n".join(routes))
    yield


app = FastAPI(
    title="FluidAI Enterprise Assistant",
    description="AI-powered enterprise assistant with tool calling for ACME Corp employees.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(v1_router, prefix="/api/v1")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug("Incoming: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.debug("Response: %s %s -> %s", request.method, request.url.path, response.status_code)
    return response


@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to the FluidAI Enterprise Assistant!"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "version": "1.0.0"}
