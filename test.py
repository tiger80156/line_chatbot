import hashlib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = hashlib.sha1(password).hexdigest()
    def __repr__(self):
        return "User('{}','{}', '{}')".format(
            self.name,
            self.username,
            self.password
        )

class Table2(Base):
    __tablename__ = ""


if __name__ == '__main__':
    ''' 此時只有建立 SQLAlchemy Engine 實例，還沒在記憶體內建立資料，
        只有第一個 SQL 指令被下達時，才會真正連接到資料庫內執行 '''
    engine = create_engine('mysql+pymysql://root:hellohello@localhost/world', echo=True)
    ''' 真正建立表格是使用 Base.metadata.create_all(engine) '''
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    userInfos = session.query(User).all()
    session.commit()
    session.close()
