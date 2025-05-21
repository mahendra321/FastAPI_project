from fastapi import HTTPException,Depends,status,Response, APIRouter
from fastapi.params import Body
from .. import models,utils,schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/sqlalchemy/post",
    tags=['posts']
)


#input data schema # data schema from schemas.py file
'''class postbase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating : int = None
class post(postbase):
    #id:int
class postcreate(postbase):
    pass
class postUpdate(postcreate):
    pass'''
#this comment below line: my_posts created for using intial stage
#my_posts= [{"title":"title of the post 1", "content":"content of the post 1", "id":1},{"title":"favorite food", "content":"pizza is my favourite food", "id":2}]

#db_pool used when we need to connect dictly to the db 
#global connection pool
#db_pool=ConnectionPool(conninfo="host=localhost dbname=fastapi user=postgres password=postgres")

#below get_conn using while connecting directly to the DB
'''def get_conn():
    with db_pool.connection() as conn:
        conn.row_factory=dict_row
        yield conn'''
'''#connect the data base
while True:
    try:
        with psycopg.connect(host="localhost", dbname="fastapi", user="postgres", password='postgres') as conn:
            cursor=conn.cursor()
            print("db connection was successful")
            break
    except Exception as error:
        print("connecting to database failed")
        print("Error: ",error)
        time.sleep(2)'''
#below find_post and find_index_post use while using my_post variable
'''def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        

#for deleting a post find a index 
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"]==id:
            return i'''

@router.get("/")
def root():
    return {"meesage":"Hello world"} 

#this below code used when direct db connection used
'''@app.get("/post")
def get_posts(conn = Depends(get_conn)):
    with conn.cursor() as cursor:
        cursor.execute("select * from posts")
        posts=cursor.fetchall()
    return {"data":posts}'''


#get posts using sqlalchemy(one of the ORM) used
@router.get("/all", response_model=list[schemas.PostOUT])
#@router.get("/all")
def test_post(db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit : int = 2, skip : int = 0, search: Optional[str] = ''):
    #print(current_user.user_name)
    '''posts=db.query(models.Post).filter(models.Post.owner_id == curent_user.id)''' #this for specific user created posts
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts= (db.query(models.Post, func.count(models.vote_data.post_id).label("votes")).join(models.vote_data, models.vote_data.post_id == models.Post.id, isouter=True)
    .filter(models.Post.title.contains(search))
    .group_by(models.Post.id)
    .limit(limit)
    .offset(skip)
    .all())

    #results = list ( map (lambda x : x._mapping, results) )

    return posts



'''@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: postcreate,conn= Depends(get_conn)):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO posts(title,content,published) values(%s, %s, %s) returning *;",(post.title,post.content,post.published))
        new_post = cursor.fetchone()
        conn.commit()

    return {"data": new_post}'''

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.post)
def create_post(post: schemas.postCreate, db: Session=Depends(get_db), Current_user: int = Depends(oauth2.get_current_user)):
 
   new_post = models.Post(owner_id = Current_user.id,**post.model_dump())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post


'''@app.get("/posts/latest")
def latest_post():
    print("in the latest")
    post=my_posts[len(my_posts)-1]
    return {"details":post}'''

#using ORM
@router.get("/latest")
def latest_post(db: Session=Depends(get_db), Current_user: int = Depends(oauth2.get_current_user)):
    posts=db.query(models.Post).filter(models.Post.owner_id == Current_user.id).all()
    print("in the latest")
    post=posts[len(posts)-1]
    return post

'''@app.get("/posts/{id}")
def post_id(id: int, response: Response, conn=Depends(get_conn)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = %s",((id),))
        post = cursor.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post details with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"post details": f"post details with id: {id} not found"}
    print(post)
    return {"post details": post}'''


#using Sqlalchemy ORM
@router.get("/{id}" ,response_model= schemas.PostOUT)
def post_id(id: int, db: Session=Depends(get_db), Current_user: int = Depends(oauth2.get_current_user)):
    #posts=db.query(models.Post).filter(models.Post.id==id).first()

    results = db.query(models.Post, func.count(models.vote_data.user_id).label("votes")).join(models.vote_data, models.vote_data.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if results:
        return results
    if not results:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post details with id: {id} not found")
    
    '''for post in posts:
        for i,d in post.to_dict().items():
            print(i)
            if id == i:
                return {"data":post}'''
            
           
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"post details": f"post details with id: {id} not found"}
    #print(post)
    #return {"post details": post}



'''@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, conn=Depends(get_conn)):
    with conn.cursor() as cursor:
        cursor.execute("delete from posts where id = %s returning *",((id),))
        deleted_post=cursor.fetchone()
        print(deleted_post)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)'''

# using ORM

@router.delete("/delete/{id}")
def delete_post(id: int, db: Session=Depends(get_db), Current_user:int = Depends(oauth2.get_current_user)):
    for_delete_post = db.query(models.Post).filter(models.Post.id==id)
    if for_delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} not exist')
    if for_delete_post.first().owner_id != Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not matched")
    
    for_delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    



'''@app.put("/posts/{id}")
def update_post(id: int,post: postUpdate, conn=Depends(get_conn)):
    with conn.cursor() as cursor:
        cursor.execute("update posts set title = %s, content= %s, published= %s where id = %s returning *",(post.title,post.content,post.published, str(id)))
        updated_post=cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    
    #post_dict = post.model_dump()
    #post_dict["id"]= id
    #my_posts[index]= post_dict
    return {"message": updated_post}'''

#Update post Using ORM

@router.put("/update/{id}")
def update_post(id: int, py_post: schemas.postUpdate, db: Session=Depends(get_db), Current_user:int = Depends(oauth2.get_current_user)):
    query_for_update=db.query(models.Post).filter(models.Post.id==id)
    for_update=query_for_update.first()
    if for_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"in dasebase does not found a match for id:{id}")
    if for_update.owner_id != Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not allowed to do it")
    query_for_update.update(py_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return query_for_update.first()