from PIL import Image, ImageOps
from fastapi import APIRouter, UploadFile, File
from app.common.config import conf
from dataclasses import asdict
from app.common.consts import DEVICE, YOLO_PY_PATH, CFG_PATH, PT_PATH, CLASS_PATH, OUTPU_DIR, SAVE_DIR, CONF_THRES
from datetime import datetime
import os
import subprocess
import json

router = APIRouter()

# 현재 날짜 가져오기
today = datetime.now().strftime("%Y%m%d")
c = conf()
parent_path = os.path.dirname(c.BASE_DIR) # /app

device = DEVICE
yolo_path = os.path.join(parent_path, YOLO_PY_PATH)
cfg_path = os.path.join(parent_path, CFG_PATH)
pt_path = os.path.join(parent_path, PT_PATH)
class_path = os.path.join(parent_path, CLASS_PATH)
output_dir = os.path.join(parent_path, OUTPU_DIR)
save_dir = os.path.join(parent_path, SAVE_DIR)
conf_thres = CONF_THRES

# Yolo Object Detection
@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 업로드 이미지명
    filename = file.filename
    # 원본이미지, 결과 저장 폴더 생성
    save_path = os.path.join(save_dir, filename.split(".")[0])
    output_path = os.path.join(output_dir, filename.split(".")[0])
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    # 업로드 이미지 읽기
    content = await file.read()
    # 이미지 저장할 로컬 경로
    srcFile = os.path.join(save_path, filename)

    # 업로드 이미지 저장
    with open(srcFile, "wb") as f:
        f.write(content)

    # Yolo CMD
    command = f"python {yolo_path} --cfg {cfg_path} --names {class_path} --weights {pt_path} --device {device} --source {srcFile} --output {output_path} --save-xml --conf-thres {conf_thres}"
    print("cmd =======> " + command)

    # Yolo 실행
    result = subprocess.run(command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        json_data = result.stdout.split('\n')[-2]
    else:
        print(f"커맨드 실행 실패! : {result.stdout}")
        json_data = {}

    return result