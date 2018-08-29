from sqlalchemy import Column, String
from . import Base

class userinfo(Base):
    __tablename__ = "userinfo"
    displayname = Column(String(255))
    picture_url = Column(String(255))
    status_message = Column(String(255))
    user_id = Column(String(255))

    def __init__(displayname, picture_url, status_message, user_id):
        self.displayname = displayname
        self.picture_url = picture_url
        self.status_message = status_message
        self.user_id = user_id



