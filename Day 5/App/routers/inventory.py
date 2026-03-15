# File: app/routers/inventory.py
from fastapi import APIRouter

router = APIRouter(prefix='/inventory', tags=['inventory'])


inventory_db = { 1: {'id': 1, 'name': 'Mouse'},
    2: {'id': 2, 'name': 'Keyboard'},
    3: {'id': 3, 'name': 'Monitor'},}

@router.get('/')
def list_inventory():
    return [{'id': 1, 'name': 'Mouse'}, {'id': 2, 'name': 'Keyboard'}, {'id': 3, 'name': 'Monitor'}]

@router.get('/{id}')
def get_inventory(id: int):
    inv = inventory_db.get(id)
    if inv:
        return inv
    return {'message': 'Inventory ID not found'}

@router.post( path= '/createuser/{id}',status_code=201, tags=['Inventory'],summary='Inserting new inventory')
def create_user(id: int):
    return {"message":"Hello, Going to insert new users!"} 

@router.delete( path= '/deleteuser/{id}',status_code=201, tags=['Inventory'],summary='Deleting an existing inventory')
def delete_user(id: int):
    return {"message":"Hello, Going to delete this ID!"}

