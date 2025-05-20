from fastapi import HTTPException, APIRouter, Depends, status
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix= "/votes",
    tags= ['votes']
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def votes_cast(vote: schemas.votes, db: Session=Depends(database.get_db), Current_user :int = Depends(oauth2.get_current_user)):
    vote_query=db.query(models.vote_data).filter(models.vote_data.post_id == vote.post_id, models.vote_data.user_id == Current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {Current_user.id} has already voted on post {vote.post_id}")
        new_vote =  models.vote_data(post_id = vote.post_id, user_id=Current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "successfully added a vote"}
    else:
         if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
         vote_query.delete(synchronize_session=False)
         db.commit()
         return {"Message": "Successfully deleted vote"}
         
