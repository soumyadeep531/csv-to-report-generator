import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health, report, web

app = FastAPI(
    title="CSV to EDA & ML Report Generator",
    description="Automated Exploratory Data Analysis and Machine Learning Baseline Report Generator",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular routers
app.include_router(web.router)
app.include_router(health.router)
app.include_router(report.router)


def start():
    """
    Single-command entrypoint to start the server.
    """
    print("=" * 60)
    print("🚀 Starting CSV to Report Generator Server")
    print("📡 Web Interface: http://127.0.0.1:8000")
    print("📚 Swagger Docs:  http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()
