from fastapi import UploadFile, File
from app.common.config import conf
from dataclasses import asdict
from app.common.consts import DEVICE, YOLO_PY_PATH, CFG_PATH, PT_PATH, CLASS_PATH, OUTPU_DIR, SAVE_DIR, CONF_THRES
from datetime import datetime
import os
import cv2
import subprocess

# async def predict(file: UploadFile = File(...)):
async def predict(img_path: str):
    # 경로 설정
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

    # 업로드 이미지명
    filename = img_path.split("/")[-1]
    # 원본이미지, 결과 저장 폴더 생성
    save_path = os.path.join(save_dir, filename.split(".")[0])
    output_path = os.path.join(output_dir, filename.split(".")[0])
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    # 업로드 이미지 읽기
    # content = await file.read()
    img = cv2.imread(img_path)

    # 이미지 저장할 로컬 경로
    srcFile = os.path.join(save_path, filename)

    # 업로드 이미지 저장
    # with open(srcFile, "wb") as f:
    #     f.write(content)
    cv2.imwrite(srcFile, img)

    # Yolo CMD
    command = f"python {yolo_path} --cfg {cfg_path} --names {class_path} --weights {pt_path} --device {device} --source {srcFile} --output {output_path} --save-xml --conf-thres {conf_thres}"
    print("cmd =======> " + command)

    # Yolo 실행
    result = subprocess.run(command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # yolo_rst = YoloDto()
    # if result.returncode == 0:
    #     json_str = str(result.stdout).replace("\n", "").replace("\'","\"")
    #     json_data = json.loads(json_str)
    #     result_list = list(json_data["result"])

    #     for i in result_list:
    #         yolo_rst.set_rst_code = 0
    #         yolo_rst.set_label = i["label"]
    #         yolo_rst.set_conf = i["conf"]
    #         yolo_rst.set_x = i["x"]
    #         yolo_rst.set_y = i["y"]
    #         yolo_rst.set_w = i["w"]
    #         yolo_rst.set_h = i["h"]

    #     print(yolo_rst)
    # else:
    #     yolo_rst.set_rst_code = 1
    #     print(yolo_rst)

    return result