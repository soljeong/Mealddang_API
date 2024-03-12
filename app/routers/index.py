from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import db

router = APIRouter()

# 상태 체크용 API
@router.get("/")
async def index(session: Session = Depends(db.session)):
    return "OK"