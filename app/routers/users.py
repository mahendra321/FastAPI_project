from fastapi import HTTPException,Depends,status, APIRouter
from .. import utils,models,schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['users']
)



@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.userOut)
def usersignup(user_info:schemas.userCration, db: Session=Depends(get_db)):
    hashed_password=utils.hash(user_info.password)
    user_info.password = hashed_password
    new_user_creation = models.users(**user_info.model_dump())

    db.add(new_user_creation)    
    db.commit()
    db.refresh(new_user_creation)
    return new_user_creation

#get the specific user 
@router.get("/{id}", response_model=schemas.userOut)
def find_user(id: int, db: Session=Depends(get_db)):
    user_data=db.query(models.users).filter(models.users.id==id)
    if user_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id no : {id} not found")
    return user_data