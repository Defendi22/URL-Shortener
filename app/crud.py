import random
import string

from sqlalchemy.orm import Session

from app import models
from app.config import settings


def generate_short_code(length: int = settings.code_length) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=length))


def get_url_by_code(db: Session, short_code: str) -> models.URL | None:
    return db.query(models.URL).filter(
        models.URL.short_code == short_code,
        models.URL.is_active == True,
    ).first()


def get_url_by_original(db: Session, original_url: str) -> models.URL | None:
    return db.query(models.URL).filter(
        models.URL.original_url == original_url,
        models.URL.is_active == True,
    ).first()


def create_short_url(db: Session, original_url: str) -> models.URL:
    existing = get_url_by_original(db, original_url)
    if existing:
        return existing

    for _ in range(5):
        code = generate_short_code()
        if not get_url_by_code(db, code):
            break
    else:
        raise RuntimeError("Não foi possível gerar um código único após 5 tentativas")

    db_url = models.URL(original_url=original_url, short_code=code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def register_access(db: Session, url: models.URL) -> None:
    access = models.Access(url_id=url.id)
    db.add(access)
    db.commit()