import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)

    posts = relationship('Post', backref='user', lazy=True)
    comments = relationship('Comment', backref='author', lazy=True)
    following = relationship('Follower', foreign_keys='Follower.user_from_id', backref='follower', lazy='dynamic')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', backref='followed', lazy='dynamic')

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    comments = relationship('Comment', backref='post', lazy=True)
    media = relationship('Media', backref='post', lazy=True)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', 'audio', name='media_type'))
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

def to_dict(self):
    return {}

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
