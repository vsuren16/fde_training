#1
# from fastapi import FastAPI 
 
# app = FastAPI(title = "Suren App")
 
# def root():
#     return{"message":"Hello, FastAPI!"}

# from fastapi import FastAPI 
 
# app = FastAPI(title = "Suren App")

# @app.get("/")
# def root():
#     return{"message":"Hello, FastAPI!"}

# @app.get("/items")
# def read_items():
#     return [{"item_id": "Food"},{"item_id": "Bar"}]
    
# doc = {
#     '1': 'Apple',
#     '2': 'Orange'
# }

# #@app.get("/itemnames/{item_id}")

# # def itemnames(item_id: str):
# #     if item_id not in doc:
# #         raise HTTPException(status_code=404, detail="Item not found")
# #     else:
# #         return {"item_name": doc[item_id]}

# @app.get('/itemnames/{item_id}', tags=['itemlist','orderlist'], summary='Item Summary') 

# def itemnames(item_id: str):
#     if item_id not in doc:
#         raise HTTPException(status_code=404, detail="Item not found")
#     else:
#         return {"item_name": doc[item_id]}
        

# # @app.get('/health', tags=['Health'], summary='Health check')
# # def health():
# #     return {'status': 'ok'}

# payload = {
#     '1': 'Apple',
#     '2': 'Orange'
# }

# @app.post( path= '/itemsinclude',status_code=201, tags=['Items'],summary='Create a new item')
# def create_item(payload: dict):
#     if "name" not in payload: 
#         raise HTTPException(status_code=400, detail = 'name is required')
#     return {
#         "message": item_id
#     }

#Day 6 
#Miraj Github folder link - 24-FastAPI/fastapi_project/app

# from fastapi import FastAPI, HTTPException

# app = FastAPI(title= "FastAPI Basic - Learning Mode",
# description = 'API for learning FastAPI',
# version = '1.0.1')

# @app.get("/")
# def root():
#     return {"message": "Welcome to FastAPI basics"}

#2. Using Routers 


# from fastapi import FastAPI, HTTPException
# from App.routers.users import router as users_router

# app = FastAPI(title= "FastAPI Basic - Learning Mode",
# description = 'API for learning FastAPI',
# version = '1.0.1')

# app.include_router(users_router)

# @app.get("/")
# def root():
#     return {"message": "Welcome to FastAPI - Router basics"}

#3. Using Routers - User and Inventory


from fastapi import FastAPI, HTTPException
#from App.routers.users import router as users_router
from App.routers.users.v1 import router as v1_router
from App.routers.users.v2 import router as v2_router
from App.routers.inventory import router as inventory_router
from App.routers.items import router as items_router
from App.schemas import router as schemas_router
from App.schemas import *

app = FastAPI(title= "FastAPI Basic - Learning Mode",
description = 'API for learning FastAPI',
version = '1.0.1')

app.include_router(v1_router,prefix='/v1')
app.include_router(v2_router,prefix='/v2')
app.include_router(inventory_router)
app.include_router(items_router)
app.include_router(schemas_router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI - Router basics"}

DB: dict[int,dict] = {}
NEXT_ID: int = 1

app = FastAPI(title = 'FULL Pydantic demo',version = "1.0")

@app.post(path= "/items", response_model = ItemRead, status_code = 201)
def create_item(item: ItemCreate):
    global NEXT_ID
    record = item.model_dump()
    record["id"] = NEXT_ID
    DB[NEXT_ID] = record 
    NEXT_ID += 1
    return record

@app.get(path= "/items", response_model=List[ItemRead])
def list_items():
    return list(DB.values())


@app.head("/items")
def items_check():
    if not DB:
        raise HTTPException(status_code=404, detail="No items")
    return {}

@app.get( path = "/items/{item_id}", response_model = ItemRead,  status_code = 201)
def filter_item(item_id: int):
    if item_id in DB:
        return DB[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item Not Found")

@app.put( path = "/items/{item_id}", response_model = ItemRead,  status_code = 201)
def filter_item(item_id: int, price: float, name: str, description:  str):
    if item_id in DB:
        DB[item_id]["price"] = price
        DB[item_id]["name"] = name
        DB[item_id]["description"] = description
        return DB[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item Not Found")

@app.delete( path = "/items/{item_id}", response_model = ItemRead,  status_code = 201)
def delete_item(item_id: int):
    if item_id in DB:
        deleted_item = DB.pop(item_id)  # Remove the item from DB
        return deleted_item
    else:
        raise HTTPException(status_code=404, detail="Item Not Found")

##Error handling printing 


app = FastAPI()

record = { 'id':1, 'name': 'Secret', 'price': 10.0, 'test_field': 'TEST NOTE' }

@app.get('/public-item', response_model = ItemRead)
def public_item():
    return record

#Exception handling
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Custom 422: 'Validation failed' + details."""
    return JSONResponse(
        status_code=422,
        content={"error":"Validation failed","details":exc.errors()}
    )