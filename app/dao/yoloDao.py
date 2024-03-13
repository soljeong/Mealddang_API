from app.database.database import engine
from app.dto.yoloDto import YoloDto
from sqlalchemy.sql import text

def insert(session, yolo_result:YoloDto):
    yolo_data = {
        "img_path": yolo_result.get_img_path,
        "result_label": yolo_result.get_label,
        "result_conf": yolo_result.get_conf,
        "result_x": yolo_result.get_x,
        "result_y": yolo_result.get_y,
        "result_w": yolo_result.get_w,
        "result_h": yolo_result.get_h,
    }
    statement = text(
        """INSERT INTO md_yolo_result (img_path, result_label, result_conf, result_x, result_y, result_w, result_h)
        VALUES(:img_path, :result_label, :result_conf, :result_x, :result_y, :result_w, :result_h)"""
    )
    session.execute(statement, yolo_data)

def get_label(label:str):
    with engine.connect() as conn:
        data = {"label": label}
        statement = text("""SELECT food_name FROM md_nut_info WHERE class = :label""")
        result = conn.execute(statement, data)
        row = result.mappings().first()
        # print(row.food_name)
        label_data = row.food_name
        return label_data

def get_upload_img(session):
    return 0
