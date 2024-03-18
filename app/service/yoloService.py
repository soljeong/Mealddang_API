from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from app.common.consts import DEVICE, YOLO_PY_PATH, CFG_PATH, PT_PATH, CLASS_PATH, OUTPU_DIR, SAVE_DIR, CONF_THRES
from app.common.config import conf
from PIL import Image
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

        # 업로드 이미지 읽기
        content = await file.read()

        # 업로드 이미지 저장할 로컬 경로
        srcFile = os.path.join(save_path, filename)

        # 업로드 이미지 저장
        with open(srcFile, "wb") as f:
            f.write(content)

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
            # json 형태로 변환
            json_data = json.loads(json_str)
            # result 리스트 가져오기
            result_list = list(json_data["result"])

            for i in result_list:
                label = i["label"]
                conf = i["conf"]
                x = i["x"]
                y = i["y"]
                w = i["w"]
                h = i["h"]

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
                print("output_path===>" + output_path)
                crop_output_path = os.path.join(output_path, crop_output_name)
                print("crop_output_path ===> " + crop_output_path)
                cv2.imwrite(crop_output_path, cropped_image)

                # img = Image.open(crop_output_path)
                # # Pillow 이미지 객체를 Bytes로 변환
                # imgByteArr = io.BytesIO()
                # img.save(imgByteArr, format=img.format)
                # imgByteArr = imgByteArr.getvalue()
                # # Base64로 Bytes를 인코딩
                # encoded = base64.b64encode(imgByteArr)
                # # Base64로 ascii로 디코딩
                # decoded = encoded.decode('ascii')
                result_yolo.append(crop_output_name)

            # else:
            #     rst_list
        # 딕셔너리를 JSON 문자열로 변환
        response_rst["images"] = result_yolo
        json_str = json.dumps(response_rst)
        return JSONResponse(json_str)
    
    def crop_img(img, save_path: str, output_path: str):
        label = img["label"]
        conf = img["conf"]
        x = img["x"]
        y = img["y"]
        w = img["w"]
        h = img["h"]

        # 원본 이미지 가져와서 관심 영역 자르기
        image = cv2.imread(save_path)
        cropped_image = image[y:y+h, x:x+w]

        # 자른 이미지 보기
        # cv2.imshow('Cropped Image', cropped_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 자른 이미지 저장
        foldername = os.path.splitext(output_path)[-1]
        crop_output_name = f"/{foldername}_{label}_{x}_{y}_{w}_{h}_{conf}" + ".jpg"
        crop_output_path = os.path.join(save_path, crop_output_name)
        crop_result_img = cv2.imwrite(crop_output_path, cropped_image)

        return crop_result_img
