from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Numeric,
)
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship

from app.database.database import Base

class YoloResult(Base):
    __tablename__ = "md_yolo_result"

    result_id = Column(Integer, primary_key=True, autoincrement=True)
    img_path = Column(
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql"), nullable=True
    )
    result_label = Column(
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql"), nullable=True
    )
    result_conf = Column(Numeric(precision=7, scale=2), nullable=True)
    result_x = Column(Integer, nullable=True)
    result_y = Column(Integer, nullable=True)
    result_w = Column(Integer, nullable=True)
    result_h = Column(Integer, nullable=True)


