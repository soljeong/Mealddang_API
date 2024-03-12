from fastapi import FastAPI
from dataclasses import asdict
from app.database.database import db
from app.routers import predict, index
from app.common.config import conf

import uvicorn

def create_app():

    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    # db.init_app(app, **conf_dict)
    
    # 데이터 베이스 연결

    # 미들웨어

    # 라우터
    app.include_router(predict.router)
    app.include_router(index.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
