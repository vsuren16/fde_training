# File: app/routers/items.py (path params example)
from fastapi import APIRouter, Path, Query

#router = APIRouter(prefix='/items', tags=['items'])
router = APIRouter(prefix='/search', tags = ['search'])

item_db = { 1: {'id': 1, 'name': 'Mouse'},
    2: {'id': 2, 'name': 'Keyboard'},
    3: {'id': 3, 'name': 'Monitor'},}


@router.get('/search')
def search_items(q: str = Query(None, min_length=3, max_length=50), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    return {'q': q, 'page': page, 'limit': limit, 'results': []}


@router.get('/')
def list_item():
    return [{'id': 1, 'name': 'Mouse'}, {'id': 2, 'name': 'Keyboard'}, {'id': 3, 'name': 'Monitor'}]


@router.get('/{item_id}')
def get_item(item_id: int):
    item = item_db.get(item_id) 
    if item:
        return item
    return {'message': 'Inventory ID not found'}


@router.post( path= '/createitem/{item_id}',status_code=201, tags=['Item'],summary='Inserting new item')
def create_user(id: int):
    return {"message":"Hello, Going to insert new item!"} 

@router.delete( path= '/deleteuser/{item_id}',status_code=201, tags=['Item'],summary='Deleting an existing item')
def delete_user(id: int):
    return {"message":"Hello, Going to delete this ID!"}
