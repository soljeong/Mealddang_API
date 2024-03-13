from fastapi import APIRouter, UploadFile, File
from app.service.yoloService import *
from app.dto.webRequest import WebRequest
from app.dto.webResponse import WebResponse

router = APIRouter()

# @router.post("/predict")
@router.post(
        "/predict",
        response_model=int)
async def post_predict(img_path: str = "C:/Users/Playdata/Desktop/test/test2.jpg"):
    return await YoloService().service_yolo(img_path)