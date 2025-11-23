from fastapi import FastAPI, HTTPException,status,Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

users = {
    1: {
        "name": "Barangan Devon E.",
        "role": "Jr Fullstack Developer",
        "age" : "25"
    }
}


class User(BaseModel):
    name: str
    role: str
    age: int


class UpdateUser(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    age: Optional[int] = None


@app.get("/")
def root():
    return {"messages": "Hello Bai It Works!"}

@app.get("/users")
def get_all_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id:int = Path(..., description="Get the users"), gt=0, lt=100):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User Not Found")
    return users[user_id]

@app.post('/create_user/{user_id}', status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:User):
    if user_id in users:
        raise HTTPException(status_code=404, detail="User already exist")
    
    users[user_id] = user.model_dump()
    return user

@app.put("/users/${user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User is not here")
    
    current_user = users[user_id]

    if user.name is not None:
        current_user["name"] = user.name
    if user.age is not None:
        current_user["age"] = user.age
    if user.role is not None:
        current_user["role"] = user.role
    
    return current_user



@app.delete("/users/${user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="No user here")
    
    delete_user = users.pop(user_id)
    return {"message":"User has been deleted","Deleted user": delete_user}