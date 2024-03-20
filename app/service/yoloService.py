from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from app.common.consts import DEVICE, YOLO_PY_PATH, CFG_PATH, PT_PATH, CLASS_PATH, OUTPU_DIR, SAVE_DIR, CONF_THRES
from app.common.config import conf
from PIL import Image, ImageOps
import numpy as np
import subprocess
import base64
import json
import io
import os
import cv2

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

class YoloService:
    def __init__(self):
        pass

    async def service_yolo(self, file: UploadFile = File(...)):
        # 업로드 이미지명
        filename = file.filename

        # 업로드 이미지, 결과 저장 폴더 생성 (이미지명)
        save_path = os.path.join(save_dir, filename.split(".")[0])
        output_path = os.path.join(output_dir, filename.split(".")[0])
        os.makedirs(save_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)

        print("output_path===>" + output_path)

        # 업로드 이미지 읽기
        content = await file.read()
        print(type(content))

        # 업로드 이미지 저장할 로컬 경로
        srcFile = os.path.join(save_path, filename)

        # 업로드 이미지 저장
        # with open(srcFile, "wb") as f:
        #     f.write(content)

        print(type(srcFile))
        srcFile = resize_image(content, srcFile)

        # Yolo CMD
        command = f"python {yolo_path} --cfg {cfg_path} --names {class_path} --weights {pt_path} --device {device} --source {srcFile} --output {output_path} --save-xml --conf-thres {conf_thres}"
        print("cmd =======> " + command)

        # Yolo 실행
        result = subprocess.run(command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(result.returncode)

        # Yolo 결과 정제
        response_rst = {}
        result_yolo = []
        if result.returncode == 0:
            # json 에서 줄바꿈 삭제
            json_str = str(result.stdout).replace("\n", "").replace("\'","\"")
            print("json_str =======> " + json_str)
            # json 형태로 변환
            json_data = json.loads(json_str)
            # result 리스트 가져오기
            result_list = list(json_data["result"])

            print("추출 결과 갯수 =====> " + str(len(result_list)))
            for i in result_list:
                crop_output_name = crop_img(i, srcFile, output_path, filename)
                result_yolo.append(crop_output_name)

            # else:
            #     rst_list
        result_yolo_distinct = list(set(result_yolo))
        # 딕셔너리를 JSON 문자열로 변환
        response_rst["images"] = result_yolo_distinct
        json_str = json.dumps(response_rst)
        print("result json_str =======> " + json_str)
        return JSONResponse(json_str)
    
def crop_img(img, srcFile: str, output_path: str, filename: str):
    label = img["label"]
    conf = img["conf"]
    x = img["x"]
    y = img["y"]
    w = img["w"]
    h = img["h"]

    # 원본 이미지 가져와서 관심 영역 자르기
    image = cv2.imread(srcFile)
    cropped_image = image[y:y+h, x:x+w]

    # 자른 이미지 보기
    # cv2.imshow('Cropped Image', cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 자른 이미지 저장
    foldername = filename.split(".")[0]
    conf_int = str(conf).split(".")[-1]
    crop_output_name = f"{foldername}_{label}_{x}_{y}_{w}_{h}_{conf_int}" + ".jpg"
    crop_output_path = os.path.join(output_path, crop_output_name)
    print("crop_output_path ===> " + crop_output_path)
    cv2.imwrite(crop_output_path, cropped_image)

    return crop_output_name

def resize_image(content, srcFile: str):
    # byte로 읽어들인 이미지를 numpy 배열로 변환
    nparr = np.frombuffer(content, np.uint8)

    # numpy 배열을 OpenCV 이미지로 변환
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 원하는 크기로 이미지 크기 조절
    new_width, new_height = 1024, 1024
    resized_image = cv2.resize(image, (new_width, new_height))

    # 조절된 이미지를 byte로 변환
    success, encoded_image = cv2.imencode('.jpg', resized_image)
    resized_image_bytes = encoded_image.tobytes()

    # byte를 파일로 저장하거나 다른 용도로 사용 가능
    with open(srcFile, "wb") as f:
        f.write(resized_image_bytes)
    
    return srcFile