from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional, Annotated

class postBase(BaseModel):
    title: str
    content: str
    published: bool = True




class postCreate(postBase):
    pass
class postUpdate(postBase):
    pass

class userOut(BaseModel):
    id: int
    user_name: EmailStr
    created_at : datetime
    '''class congig:
        orm_mode=True'''
#below class for practice
'''class user_yoyo(BaseModel):
    id: int
    user_name: EmailStr
    created_at : datetime
    password : str
    class config:
        orm_mode=True'''
    
    
class post(postBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : userOut
    # id: int
    #title: str
    #content: str
    #published: bool
    #class config:
    """orm_mode = True"""
class PostOUT(BaseModel):
    Post: post
    votes : int
    '''class Config:
        orm_mode = True'''


class userCration(BaseModel):
    user_name : EmailStr
    password : str



class userLogin(BaseModel):
    user_name : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str
class TokenData(BaseModel):
    id: int

class votes(BaseModel):
    post_id : int
    dir : Annotated[int, Field(strict=True, le=1)]