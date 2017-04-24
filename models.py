from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///app_data.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    url = Column(String(2000), nullable=False)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Site :%r>" % self.url

    @property
    def serialize(self):
        return {'id': self.id, 'url': self.url}


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    up = Column(Boolean, nullable=False)
    code = Column(Integer)
    time_taken = Column(Float)
    site_id = Column(Integer, ForeignKey('sites.id'))
    site = relationship(Site)

    def __init__(self, site, up, code=None, time_taken=None):
        self.up = up
        self.code = code
        self.time_taken = time_taken
        self.site = site

    def __repr__(self):
        return "<Response :%r:%r>" % (self.site.url, self.up)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'time_stamp': self.time_stamp,
            'up': self.up,
            'code': self.code,
            'time_taken': self.time_taken,
            'site': self.site.serialize
        }


if __name__ == '__main__':
    engine = create_engine('sqlite:///app_data.db')
    Base.metadata.create_all(bind=engine)
