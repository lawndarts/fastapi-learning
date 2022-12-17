

from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, oauth2
from ..database import engine,  get_db
from sqlalchemy.orm import Session 
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", #ex allows routes to be /{id} vs /posts/{id}
    tags=['Posts'] #groups this type of route in fastapi documentation
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#note, the current_user is specified as an INT, when the function will return a user object.
#this doesnt seem to matter. It seems like it can just be deleted safely. 

    #This is left to show how to query with raw sql.
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    #You could add the filter function after Models.post) to filter for only posts made by
    #the current user
    #old "get all posts" query
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return posts

#string sanitization handled with the %s placeholders with real data in the second argument
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published))
    # newpost = cursor.fetchone()
    # conn.commit()
    newpost = models.Post(owner_id=current_user.id, **post.dict())#wow. that easy huh
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost

#id is validated as an int, then casted back to a string to work with DB
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, str(id),)#heres the mystery comma
    # post = cursor.fetchone()
    #old query
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id({id}) was not found') 
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):#, status_code=status.HTTP_204_NO_CONTENT (instructor used this as a second parameter but i dont think its necessary for now)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id),)#mystery comma. leaving them in for now
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id({id}) was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return (Response(status_code=status.HTTP_204_NO_CONTENT))#https://youtu.be/0sOvCWFmrtA?t=7712 explains this nonsense (a little before the timestamp
    #okay im wondering how we send back additional information along with this status code
    

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #  (post.title, post.content, post.published, str(id)),)
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id({id}) was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")

    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()
