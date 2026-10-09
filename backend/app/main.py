from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.database import engine, Base
from backend.app.api.jobs import router as jobs_router
from backend.app.api.settings import router as settings_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FilePilot API",
    description="Intelligent File Organizer Backend API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router, prefix="/api")
app.include_router(settings_router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FilePilot API v1.0"}


# Serve static React frontend files in single-service cloud deployments
dist_dir = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if dist_dir.is_dir():
    assets_dir = dist_dir / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        target_path = (dist_dir / full_path).resolve()
        if not target_path.is_relative_to(dist_dir):
            raise HTTPException(status_code=404, detail="Not found")
        if target_path.is_file():
            return FileResponse(target_path)
        return FileResponse(dist_dir / "index.html")
