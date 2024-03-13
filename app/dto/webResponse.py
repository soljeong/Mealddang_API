from pydantic import BaseModel, Field
from app.dto.webRequest import WebRequest

class WebResponse(BaseModel):
    img_path: str = Field(..., title="요청 이미지 경로 _중복 가능")
    result_label: str = Field(..., title="결과 label")
    result_conf: float = Field(..., title="결과 conf")
    result_x: int = Field(..., title="결과 x_point")
    result_y: int = Field(..., title="결과 y_point")
    result_w: int = Field(..., title="결과 width")
    result_h: int = Field(..., title="결과 height")
