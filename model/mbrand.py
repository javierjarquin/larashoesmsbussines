from sqlalchemy import Column, Integer, String
from config.connection import Base

class Brand(Base):
    __tablename__ = 'brand'

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)

    def __init__(self, name=""):
        self.name = name