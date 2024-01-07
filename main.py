import model.mbrand
import model.mmodel
import model.mproduct
import model.mprovider
import base64
import io
from fastapi import FastAPI, HTTPException, Depends, status
from config.connection import engine, session
from sqlalchemy.orm import Session
from ftplib import FTP

app = FastAPI()
model.mbrand.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

###
### Controladores
###
def putFile(fileName, fileContent):
    try:
        ftp = FTP('127.0.0.1')
        ftp.login(user='FTP_Lara', passwd='lara1234*')

        buffer = io.BytesIO(fileContent)
        buffer.seek(0)

        ftp.storbinary(f'STOR {fileName}', buffer)

        print(f"El archivo {fileName} se ha subido correctamente")
        ftp.quit()
    except Exception as e:
        print(f"Error al subir archivo al servidor FTP {e}")
### Marcas
def createBrand(db: Session, name:str):
    brand = model.mbrand.Brand(name=name)
    db.add(brand)
    db.commit()
    return {"status": "Marca creada correctamente"}

def getBrand(db: Session, name: str):
    if name:
        brand = db.query(model.mbrand.Brand).filter(model.mbrand.Brand.name.like(f"%{name}%")).all()
    else:
        brand = db.query(model.mbrand.Brand).all()
    return brand

def getBrandById(db: Session, brandId: int):
    brand = db.query(model.mbrand.Brand).filter(model.mbrand.Brand.id == brandId).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return brand
### Fin Marcas
### Modelos
def createModel(db: Session, brandId: str, name: str, version: str, gender: str, file_base64: str = None):
    try:
        if file_base64:
            decode_file = base64.b64decode(file_base64)
            putFile(f"{name}_{version}.jpg", decode_file)

        models = model.mmodel.Model(brandId=brandId, name=name, version=version, gender=gender)
        db.add(models)
        db.commit()
        return {"status": "Se ha creado correctamente el modelo"}
    except Exception as e:
        return {"error": f"Error al procesar archivos: {e}"}

def getModel(db: Session, brandId: str, name: str, version: str, gender: str):
    models = db.query(model.mmodel.Model)
    if brandId:
        models = models.filter(model.mmodel.Model.brandId == brandId)
    if name:
        models = models.filter(model.mmodel.Model.name.like(f"%{name}%"))
    if version:
        models = models.filter(model.mmodel.Model.version.like(f"%{version}%"))
    if gender:
        models = models.filter(model.mmodel.Model.gender == gender)

    modelList = models.all()
    return modelList

def getModelById(db: Session, modelId: int):
    model_Id = db.query(model.mmodel.Model).filter(model.mmodel.Model.id == modelId).first()
    if not model_Id:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    return model_Id
### Fin modelos
### Productos

def createProduct(db: Session, name: str, description: str, modelId: str, typeProduct: str, status: str, unit: str):
    product = model.mproduct.Product(name=name, description=description, modelId=modelId, typeProduct=typeProduct, status=status, unit=unit)
    db.add(product)
    db.commit()
    return {"status": "se ha creado correctamente el producto"}

def getProduct(db: Session, name: str, description: str, modelId: str, typeProduct: str, status: str, unit: str):
    products = db.query(model.mproduct.Product)
    if name:
        products = products.filter(model.mproduct.Product.name.like(f"%{name}%"))
    if description:
        products = products.filter(model.mproduct.Product.description.like(f"%{description}%"))
    if modelId:
        products = products.filter(model.mproduct.Product.modelId == modelId)
    if typeProduct:
        products = products.filter(model.mproduct.Product.typeProduct == typeProduct)
    if status:
        products = products.filter(model.mproduct.Product.status == status)
    if unit:
        products = products.filter(model.mproduct.Product.unit == unit)

    productList = products.all()
    return productList

def getProductById(db: Session, productId: int):
    product_Id = db.query(model.mproduct.Product).filter(model.mproduct.Product.id == productId).first()
    if not product_Id:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product_Id
### Fin Productos
### Proveedores

def createProvider(db: Session, commercialName: str, fiscalName: str, rfc: str, address: str, phone: str, isCredit: int, creditDay: int, typeProvider: str, account: str):
    provider = model.mprovider.Provider(commercialName=commercialName, fiscalName=fiscalName, rfc=rfc, address=address, phone=phone, isCredit=isCredit, crediDay=creditDay, typeProvider=typeProvider, account=account)
    db.add(provider)
    db.commit()
    return {"status": "se ha creado correctamente el proveedor"}

def getProvider(db: Session, commercialName: str, fiscalName: str, rfc: str, address: str, phone: str, isCredit: int, creditDay: int, typeProvider: str, account: str):
    providers = db.query(model.mprovider.Provider)
    if commercialName:
        providers = providers.filter(model.mprovider.Provider.commercialName.like(f"%{commercialName}%"))
    if fiscalName:
        providers = providers.filter(model.mprovider.Provider.fiscalName.like(f"%{fiscalName}%"))
    if rfc:
        providers = providers.filter(model.mprovider.Provider.rfc.like(f"%{rfc}%"))
    if address:
        providers = providers.filter(model.mprovider.Provider.address.like(f"%{address}%"))
    if phone:
        providers = providers.filter(model.mprovider.Provider.phone.like(f"%{phone}%"))
    if isCredit:
        providers = providers.filter(model.mprovider.Provider.isCredit == isCredit)
    if typeProvider:
        providers = providers.filter(model.mprovider.Provider.typeProvider == typeProvider)

    providerList = providers.all()
    return  providerList

def getProviderById(db: Session, providerId: int):
    provider_Id = db.query(model.mprovider.Provider).filter(model.mprovider.Provider.id == providerId).first()
    if not provider_Id:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return provider_Id
### Fin Proveedores
###
### Fin Controladores
###

###
### Rutas
###

### Marcas
@app.post("/createBrand/")
async def newBrand(name: str=None, db: Session = db_dependency):
    return createBrand(db, name)

@app.get("/brands/")
async def getbrands(name: str=None, db: Session = db_dependency):
    return getBrand(db, name)

@app.get("/brand/{brandId}")
async def getBrandId(brandId: int=None, db: Session = db_dependency):
    return getBrandById(db, brandId)
### Fin Marcas
### Modelos
@app.post("/createModel/")
async def newModel(brandId: str=None, name: str=None, version: str=None, gender: str=None, file_base64: str = None,db: Session = db_dependency):
    return createModel(db, brandId, name, version, gender, file_base64)

@app.get("/models/")
async def getModels(brandId: str=None, name: str=None, version: str=None, gender: str=None, db: Session = db_dependency):
    return getModel(db, brandId, name, version, gender)

@app.get("/model/{modelId}")
async def getModelId(modelId: int=None, db: Session = db_dependency):
    return getModelById(db, modelId)
### Fin Modelos
### Productos

@app.post("/createProduct/")
async def newProduct(name: str=None, description: str=None, modelId: str=None, typeProduct: str=None, status: str=None, unit: str=None, db: Session = db_dependency):
    return createProduct(db, name, description, modelId, typeProduct, status, unit)

@app.get("/products/")
async def getProducts(name: str=None, description: str=None, modelId: str=None, typeProduct: str=None, status: str=None, unit: str=None, db: Session = db_dependency):
    return getProduct(db, name, description, modelId, typeProduct, status, unit)

@app.get("/product/{productId}")
async def getProductId(productId: int=None, db: Session = db_dependency):
    return getProductById(db, productId)

### Fin Productos
### Proveedores

@app.post("/createProvider/")
async def newProvider(commercialName: str, fiscalName: str, rfc: str, address: str, phone: str, isCredit: int=0, creditDay: int=0, typeProvider: str='FI', account: str='', db: Session = db_dependency):
    return createProvider(db, commercialName, fiscalName, rfc, address, phone, isCredit, creditDay, typeProvider, account)

@app.get("/providers/")
async def getProviders(commercialName: str=None, fiscalName: str=None, rfc: str=None, addres: str=None, phone: str=None, isCredit: int=None, creditDay: int=None, typeProvider: str=None, account: str=None, db: Session = db_dependency):
    return getProvider(db, commercialName, fiscalName, rfc, addres, phone, isCredit, creditDay, typeProvider, account)

@app.get("/provider/{providerId}")
async def getProviderId(providerId: int, db: Session = db_dependency):
    return getProviderById(db, providerId)

### Fin Proveedores
###
### Fin Rutas
###
