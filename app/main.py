from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path
# libs
from app import crud, models
from app.config import settings
from app.database import Base, engine, get_db
from app.schemas import URLCreate, URLResponse, URLStats

app = FastAPI(title="URL Shortener", version="1.0.0")

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    db_url = crud.create_short_url(db, original_url=str(payload.original_url))
    return URLResponse(
        short_code=db_url.short_code,
        short_url=f"{settings.base_url}/{db_url.short_code}",
        original_url=db_url.original_url,
        created_at=db_url.created_at,
    )


@app.get("/stats/{short_code}", response_model=URLStats)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL não encontrada")
    return db_url


@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL não encontrada")
    crud.register_access(db, db_url)
    return RedirectResponse(url=db_url.original_url, status_code=302)