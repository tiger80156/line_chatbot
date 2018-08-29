from sqlalchemy import Column, String, Integer
from . import Base

class userinfo(Base):
    __tablename__ = "userinfo"
    displayname = Column(String(255))
    picture_url = Column(String(255))
    status_message = Column(String(255))
    user_id = Column(String(255), primary_key = True)

    def __init__(self,displayname, picture_url, status_message, user_id):
        self.displayname = displayname
        self.picture_url = picture_url
        self.status_message = status_message
        self.user_id = user_id

    def __repr__(self):
        return "userinfo('{}','{}','{}',{})".format(
            self.displayname,
            self.picture_url,
            self.status_message,
            self.user_id
        )

