from pydantic import BaseModel, Field

class WebRequest(BaseModel):
    # result_id: int = Field(..., title="결과 id_PK")
    img_path: str = Field(..., title="요청 이미지 경로")
