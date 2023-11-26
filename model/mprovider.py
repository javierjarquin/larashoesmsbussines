from sqlalchemy import Column, Integer, String
from config.connection import Base

class Provider(Base):
    __tablename__ = 'provider'

    id             = Column(Integer, primary_key=True, index=True)
    commercialName = Column(String(300), nullable=False)
    fiscalName     = Column(String(300), nullable=False)
    rfc            = Column(String(20), nullable=False)
    address        = Column(String(350), nullable=False)
    phone          = Column(String(15), nullable=False)
    isCredit       = Column(Integer, default=0)
    creditDay      = Column(Integer, default=0)
    typeProvider   = Column(String(2), nullable=False)
    account        = Column(String(20), nullable=True)

    def __init__(self, commercialName="", fiscalName="", rfc="", address="", phone="", isCredit=None, crediDay=None, typeProvider="", account=""):
        self.commercialName = commercialName
        self.fiscalName     = fiscalName
        self.rfc            = rfc
        self.address        = address
        self.phone          = phone
        self.isCredit       = isCredit
        self.creditDay      = crediDay
        self.typeProvider   = typeProvider
        self.account        = account