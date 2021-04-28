from datetime import datetime, timedelta 
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from app.database import Base 
import jwt 


class DefaultMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id= Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow ) 
    modified_at = Column(DateTime, onupdate=datetime.utcnow )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

class User(DefaultMixin, Base):
    __tablename__ = "users"
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(1024), nullable=False)
    verified = Column(Boolean, default=False)
    
    colors = relationship('Color', backref="user")
    tags = relationship('Tag', backref="user")


    def __init__(self, username : str, password : str ):
        self.username = username
        self.password = generate_password_hash((password))

    def __repr__(self):
        return f"<User {self.username}>"

    def verify_password( self, password: str ):
        return check_password_hash(self.password, password)


    @staticmethod
    def verify_token( token, check_expire:bool =True):
        from run import app
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"],
         options={"verify_exp": check_expire, "requires":["id"]} ) 
        return User.query.get(payload["id"])

    def generate_token( self, expire=None ):
        from run import app 
        if not expire : expire = app.config["TOKEN_LIFETIME_IN_SECONDS"]
        payload = {
            "id": self.id,
            "exp": datetime.utcnow() + timedelta(seconds=expire) 
        } 
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return token 


class Color(DefaultMixin, Base):
    __tablename__ = "colors"
    name = Column(String(255), nullable=False)
    description = Column(Text)
    rating = Column(Integer, default=0)
    code = Column(String(7), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id',  onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    tags = relationship('ColorTags', backref="color")

    __table_args__ = (UniqueConstraint('name', 'user_id', name='_user_colorname_uc'),)

    def __repr__(self):
        return f"<Color {self.code}>"


class Tag(DefaultMixin, Base):
    __tablename__ = "tags"
    name = Column(String(32), nullable=False)
    color = Column(String(7), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id',  onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    colors = relationship('ColorTags',  backref="tag")
    
    __table_args__ = (UniqueConstraint('name', 'user_id', name='_user_tagname_uc'),)

    def __repr__(self):
        return f"<Tag {self.name}>"


class ColorTags( DefaultMixin, Base):
    __tablename__ ="color_tags"
    color_id = Column(Integer, ForeignKey("colors.id",onupdate="CASCADE", ondelete="CASCADE" ) , nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False ) 

    __table_args__ = (UniqueConstraint('color_id', 'tag_id', name='_user_colortags_uc'),)

class LoggedOutToken( DefaultMixin, Base):
    __tablename__ = "expired_tokens"
    token = Column(String(1024))
