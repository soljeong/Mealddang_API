from fastapi import APIRouter
from app.database.database import *
from sqlalchemy.sql import text

router = APIRouter()

# 상태 체크용 API
@router.get("/")
def index():
    return "OK"

@router.get("/db")
async def index():
    session = SessionLocal()
    with engine.connect() as conn:
        statement = text("""SELECT COUNT(*) FROM md_yolo_result""")
        # statement = text("""SELECT COUNT(*) FROM md_nut_info""")
        result = conn.execute(statement)
        data = result.mappings().all()
        # data = result.mappings().first()
        session.commit()
        session.close()
        return {"result": data}