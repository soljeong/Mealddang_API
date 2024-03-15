from datetime import datetime

DB_USERNAME = "mealddang"
DB_PASSWORD = "alfEkd!!!"
DB_HOST = "3.38.213.167"
DB_PORT = 3306
DB_NAME = "mealddang"

TODAY = datetime.now().strftime("%Y%m%d")
DEVICE = "cpu"
YOLO_PY_PATH = "yolov3\\detect_meal.py"
CFG_PATH = "yolov3\\cfg\\best_md_403.cfg"
PT_PATH = "yolov3\\weights\\best_md_403.pt"
CLASS_PATH = "yolov3\\data\\best_md_403_cls.names"
OUTPU_DIR = f"app\\result\\{TODAY}\\output"
SAVE_DIR = f"app\\result\\{TODAY}\\source"
CONF_THRES = 0.4