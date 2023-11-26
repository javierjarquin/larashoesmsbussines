from sqlalchemy import Column, Integer, String, ForeignKey
from config.connection import Base

class Product(Base):
    __tablename__ = 'product'

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(200), nullable=False)
    description = Column(String(350), nullable=False)
    modelId     = Column(Integer, ForeignKey('model.id'), nullable=False)
    typeProduct = Column(String(200), nullable=False)
    status      = Column(String(3), nullable=False)
    unit        = Column(String(2), nullable=False)

    def __init__(self, name="", description="", modelId=None, typeProduct="", status="", unit=""):
        self.name        = name
        self.description = description
        self.modelId     = modelId
        self.typeProduct = typeProduct
        self.status      = status
        self.unit        = unit
