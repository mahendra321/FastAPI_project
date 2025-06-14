from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2, utils

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session=Depends(database.get_db)): # user_credentials:schemas.userLogin

   user_cred = db.query(models.users).filter(models.users.user_name == user_credentials.username).first()
   if not user_cred:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"user not foud with mail_id {user_credentials.username} or invalid credentials")
   if not utils.verify(user_credentials.password,user_cred.password):
      raise HTTPException(
         status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
      ) 
   #create token
   #reurn token
   access_token = oauth2.create_access_token(data={"user_id": user_cred.id})
   return {"access_token": access_token, "token_type":"bearer"}
      