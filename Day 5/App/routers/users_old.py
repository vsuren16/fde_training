####COMMENTING FULLY TO TEST VERSIONS
'''
# File: app/routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=['users'])

users_db = { 1: {'id': 1, 'name': 'Alice'},
    2: {'id': 2, 'name': 'Bob'},
    3: {'id': 3, 'name': 'Charlie'},}

@router.get('/')
def list_users():
    return [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]

# @router.get('/{user_id}')
# def get_user(user_id: int):
#     user = users_db.get(user_id)
#     if user:
#         return user
#     return {'message': 'User not found'}

@router.get( path= '/v1/{user_id}', summary = 'Get user details with old version')
def get_user_v1(user_id: int):
    user = users_db.get(user_id)
    if user:
        return user
    return {'message': 'User not found'}

@router.get( path= '/v2/{user_id}', summary = 'Get user details with new version')
def get_user_v2(user_id: int):
    user = users_db.get(user_id)
    if user:
        return user
    return {'message': 'User not found'}

@router.post( path= '/createuser/{user_id}',status_code=201, tags=['Users'],summary='Inserting new user')
def create_user(user_id: int):
    return {"message":"Hello, Going to insert new users!"} 

@router.delete( path= '/deleteuser/{user_id}',status_code=201, tags=['Users'],summary='Deleting user')
def delete_user(user_id: int):
    return {"message":"Hello, Going to delete this ID!"}
    '''