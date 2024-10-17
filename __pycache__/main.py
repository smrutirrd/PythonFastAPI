from typing import Optional,List
from fastapi import Depends, FastAPI,Query
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session


from database import Base,engine,SessionLocal

#Model
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    is_active=Column(Boolean,default=True)
    
    

    

#Schema
class UserSchema(BaseModel):
    id:int
    email:str
    is_active:bool

    class config:
         orm_model=True

def get_db():
    db=SessionLocal()
    try:
      yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
app=FastAPI()   

@app.post("/users",response_model=UserSchema)
def index(user: UserSchema,db:Session=Depends(get_db)):
    u=User(email=user.email,is_active=user.is_active,id=user.id)
    db.add(u)
    db.commit()
    return u

@app.get("/users",response_model=List[UserSchema])
def index(db:Session=Depends(get_db)):
    return db.query(User).all()

# @app.get("/first")
# def index():
#     return "hello world"


# @app.get("/items/{item_id}")
# def index(item_id:int):
#     return {"product_id":item_id}


# # @app.get("/items/")
# # def index(q:int,m:Optional[int]=10):
# #     return {"product is":q,"m":m}

# # @app.get("/items")
# # def index(q:Optional[str]=None):
# #     return {"q":q}

# # @app.get("/items")
# # def index(q:Optional[str]=Query(None,min_length=3,max_length=5,regex="^jhj")):
# #     return {"q":q}

# @app.get("/items")
# def index(q:Optional[List[str]]=Query(["foo","bar"])):
#    return {"q":q}

# @app.get("/items/{file_path:path}")
# def index(file_path:str):
#     return {"file-path":file_path}

# @app.post("/items/{user_id}")
# def index(user_id:int,User: User):
#     return User

# @app.get("/items")
# def index():
#     return "hello world"