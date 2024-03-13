from fastapi import File, UploadFile
from app.database.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from app.utils.yolo import *
from app.dao.yoloDao import *
from app.dto.yoloDto import YoloDto
import json

class YoloService:
    def __init__(self):
        pass

    async def service_yolo(self, img_path: str):

        result = await predict(img_path)

        session = SessionLocal()
        rst_code = 1
        yolo_rst = YoloDto()
        if result.returncode == 0:
            json_str = str(result.stdout).replace("\n", "").replace("\'","\"")
            json_data = json.loads(json_str)
            result_list = list(json_data["result"])

            for i in result_list:
                rst_code = 0

                yolo_rst.set_img_path = img_path                  
                label_data = get_label(i["label"])
                yolo_rst.set_label = label_data
                yolo_rst.set_conf = i["conf"]
                yolo_rst.set_x = i["x"]
                yolo_rst.set_y = i["y"]
                yolo_rst.set_w = i["w"]
                yolo_rst.set_h = i["h"]

                insert(session, yolo_rst)
                session.commit()
                session.close()
        else:
            rst_code = 1
        
        
        return rst_code
