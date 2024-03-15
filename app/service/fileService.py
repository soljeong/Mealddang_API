from fastapi.responses import FileResponse
from app.common.config import conf
from app.common.consts import OUTPU_DIR
import os

c = conf()
parent_path = os.path.dirname(c.BASE_DIR) # /app
output_dir = os.path.join(parent_path, OUTPU_DIR)

def service_file(filename: str):
    try:
        output_folde_path = os.path.join(output_dir, filename.split("_")[0])
        print("output_folde_path========>" + output_folde_path)
        ouput_file_path = os.path.join(output_folde_path, filename)
        print("ouput_file_path========>" + ouput_file_path)
        return FileResponse(ouput_file_path)
    except FileNotFoundError:
        return {"error": "File not found"}