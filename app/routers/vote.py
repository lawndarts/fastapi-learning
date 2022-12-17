from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine,  get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/vote", #ex allows routes to be /{id} vs /posts/{id}
    tags=['Vote'] #groups this type of route in fastapi documentation
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #this just checks to see if the post exists before seeing if it has already been voted on,
    #by querying the posts table
    check = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not check: raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id{vote.post_id} does not exist"))
    #this line finds out if a user has already voted on a post
    #added second query condition by adding a comma before
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # print("this")
    if (vote.dir) == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on the post")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message": "Successfully deleted vote"}