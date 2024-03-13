from fastapi import FastAPI
from app.routers import predict, index

import uvicorn

def create_app():

    app = FastAPI()

    # 라우터
    app.include_router(predict.router)
    app.include_router(index.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
