from time import strftime, gmtime

from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

# Replace 'sqlite:///rfg.db' with your path to database
engine = create_engine('sqlite:///feeds.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def gen_offset_from_page(page, limit):
    page = int(page)
    limit = int(limit)
    if page is 0:
        page = 1
    return (page * limit) - limit

def generate_meta(limit, page, total_items):
    """
    This method help to generate links and metadata object
    :param table_view_name:
    :param limit:
    :param page:
    :param page_count:
    :return:
    """
    meta_object={}
    total_count = len(total_items) if len(total_items) is not 0 else 0
    total_pages = total_count / limit
    modulus = total_count % limit
    import re
    total_pages = int(re.sub(r"\.\d+$", '', str(total_pages))) + 1 if modulus is not 0 else total_pages
    meta_object["current"] = page
    meta_object["total_page"] = total_pages
    if total_pages > page:
        meta_object["next_page"] = page + 1
        meta_object["prev_page"] = page - 1
    else:

        meta_object["prev_page"] = page - 1

    return meta_object

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    username = Column(String(255))


class Source(Base):
    __tablename__ = 'source'
    id = Column(String(50), primary_key=True)
    object_id = Column(String(50), unique=True)
    tag = Column(String(20))
    img = Column(String(255))
    name = Column(Text, unique=True)
    base_url = Column(String(50), unique=True)
    issue = relationship("Issue", uselist=True)
    # article = relationship("Article", back_populates="source")

    created_date = Column(String(50), default=str(strftime("%a, %d %b %Y %X +0000", gmtime())))
    updated_date = Column(String(50), default=str(strftime("%a, %d %b %Y %X +0000", gmtime())))


class Issue(Base):
    __tablename__ = 'issue'
    id = Column(String(50), primary_key=True)
    object_id = Column(String(50), unique=True)
    url = Column(String(255))
    issue_number = Column(String(20))
    source_id = Column(String(255), ForeignKey("source.object_id"))

    article = relationship("Article", uselist=True)
    created_date = Column(String(50), default=str(strftime("%a, %d %b %Y %X +0000", gmtime())))
    updated_date = Column(String(50), default=str(strftime("%a, %d %b %Y %X +0000", gmtime())))


class Article(Base):
    __tablename__ = 'article'
    id = Column(String(50), primary_key=True)
    object_id = Column(String(50), unique=True)
    url = Column(String(255))
    img = Column(String(255))
    main_url = Column(String(255))
    title = Column(String(255))
    pre_content = Column(String(500))
    source_id = Column(String(255), ForeignKey("source.object_id"))
    issue_id = Column(String(255), ForeignKey("issue.object_id"))
    created_date = Column(String(50), default=str(strftime("%a, %d %b %Y %X +0000", gmtime())))
    updated_date = Column(String(50), default=str(strftime("%a, %d %b %Y %X +0000", gmtime())))
