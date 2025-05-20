from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__= "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False, default="yoyo")
    published = Column(Boolean, server_default= "True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("all_users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship('users')

class users(Base):
    __tablename__="all_users"

    id = Column(Integer,primary_key=True, nullable=False)
    user_name= Column(String,nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    phone_number = Column(String)

class vote_data(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey("posts.id", ondelete = "CASCADE"), primary_key=True)
    user_id = Column(Integer,ForeignKey("all_users.id", ondelete = "CASCADE"), primary_key= True)