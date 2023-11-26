from sqlalchemy import Column, Integer, String, ForeignKey
from config.connection import Base

class Model(Base):
    __tablename__ = 'model'

    id      = Column(Integer, primary_key=True, index=True)
    brandId = Column(Integer, ForeignKey('brand.id'), nullable=False)
    name    = Column(String(200), nullable=False)
    version = Column(String(200), nullable=False)
    gender  = Column(String(3), nullable=False)

    def __init__(self, brandId=None, name="", version="", gender=""):
        self.brandId = brandId
        self.name    = name
        self.version = version
        self.gender  = gender