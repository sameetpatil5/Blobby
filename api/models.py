from api import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(255))
    email = db.Column(String(255), unique=True)
    password = db.Column(String(255), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(Integer, primary_key=True)
    author_id = db.Column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(String(255), unique=True, nullable=False)
    subtitle = db.Column(String(255), nullable=False)
    date = db.Column(String(255), nullable=False)
    body = db.Column(Text, nullable=False)
    img_url = db.Column(String(255), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(Integer, primary_key=True)
    author_id = db.Column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id = db.Column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(Text, nullable=False)
