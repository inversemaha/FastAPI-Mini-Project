from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app.config.database import get_db
from app.models.author import Author as AuthorModel
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])

# ----------------------
# CRUD Endpoints
# ----------------------





# ----------------------
# Filter / Search Endpoints
# ----------------------