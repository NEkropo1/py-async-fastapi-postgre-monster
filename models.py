from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Dict, Any

Base = declarative_base()


class JSONFile(Base):
    __tablename__ = "json_files"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)


class JsonInput(BaseModel):
    data: Dict[str, Any]
