from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import config

# create db session
Base = declarative_base()
engine = create_engine('mysql+pymysql://root:hellohello@localhost/chatbot',echo=True)
DBSession = sessionmaker(bind=engine)
