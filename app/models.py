from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text, Boolean
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from app.database import Base 


class CommonBase(Base):
    id= Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow ) 
    modified_at = Column(DateTime, onupdate=datetime.utcnow )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

class User(CommonBase):
    __tablename__ = "users"
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(1024), nullable=False)
    verified = Column(Boolean, default=False)
    
    colors = relationship('Color', backref="user")
    tags = relationship('Tag', backref="user")


    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash((password))

    def __repr__(self):
        return f"<User {self.username}>"

    def verify_password( self, password ):
        return check_password_hash(self.password, password)


class Color(CommonBase):
    __tablename__ = "colors"
    name = Column(String(255), nullable=False)
    description = Column(Text)
    rating = Column(Integer, default=0)
    code = Column(String(7), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    tags = relationship('ColorTags')

    def __repr__(self):
        return f"<Color {code}>"


class Tag(CommonBase):
    __tablename__ = "tags"
    name = Column(String(32), nullable=False)
    color = Column(String(7), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    colors = relationship('ColorTags')

    def __repr__(self):
        return f"<Tag {name}>"


class ColorTags( CommonBase):
    __tablename__ ="color_tags"
    color_id = Column(Integer, ForeignKey("colors.id") , nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False ) 
