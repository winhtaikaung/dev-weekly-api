import datetime

from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Replace 'sqlite:///rfg.db' with your path to database
engine = create_engine('sqlite:///feeds.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    username = Column(String(255))


class Source(Base):
    __tablename__ = 'sources'
    id = Column(String(50), primary_key=True)
    object_id = Column(String(50), unique=True)
    img = Column(String(255))
    name = Column(Text)
    created_date = Column(String(50), default=str(datetime.datetime.utcnow))
    updated_date = Column(String(50), default=str(datetime.datetime.utcnow))


class Issues(Base):
    __tablename__ = 'issues'
    id = Column(String(50), primary_key=True)
    object_id = Column(String(50), unique=True)
    url = Column(String(255))
    source_id = Column(String(255), ForeignKey("sources.object_id"))
    created_date = Column(String(50), default=str(datetime.datetime.utcnow))
    updated_date = Column(String(50), default=str(datetime.datetime.utcnow))


class Articles(Base):
    __tablename__ = 'articles'
    id = Column(String(50), primary_key=True)
    object_id = Column(String(50), unique=True)
    url = Column(String(255))
    img = Column(String(255))
    pre_content = Column(String(255))
    source_id = Column(String(255), ForeignKey("sources.object_id"))
    issue_id = Column(String(255), ForeignKey("issues.object_id"))
    created_date = Column(String(50), default=str(datetime.datetime.utcnow))
    updated_date = Column(String(50), default=str(datetime.datetime.utcnow))
