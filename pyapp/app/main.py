import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api import router as api_router
from .config import get_settings


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    """
    # Add startup logic here
    yield
    # Add shutdown logic here


# Initialize FastAPI app with the lifespan manager
app = FastAPI(lifespan=lifespan)

# Include the API routers
app.include_router(api_router, prefix="/api", tags=["Scoutnet"])


# --- Static Files Configuration in production ---
# In a production Docker build, the 'client/dist' files will be copied to 'pyapp/static'
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
if os.path.exists(STATIC_DIR):  # We are running in a container
    # Mount the static directory for /assets
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    templates = Jinja2Templates(directory=STATIC_DIR)  # For templating index.html

    @app.get("/{full_path:path}", tags=["Client"])
    async def serve_react_app(request: Request, full_path: str):
        """
        Catch-all endpoint to serve the React files outside 'assets'
        """
        if not full_path:
            full_path = "index.html"
        file_path = os.path.join(STATIC_DIR, full_path)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        if full_path == "index.html":
            settings = get_settings()
            return templates.TemplateResponse(
                request=request, name="index.html", context=dict(settings)
            )  # Add environment variables
        else:
            return FileResponse(file_path)


# Add a root endpoint for basic API health check during development
@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "FastAPI server is running"}
