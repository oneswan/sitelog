from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    url = Column(String(2000), nullable=False)


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    time = Column(Float)
    site_id = Column(Integer, ForeignKey('sites.id'))
    site = relationship(Site)


if __name__ == '__main__':
    engine = create_engine('sqlite:///app_data.db')
    Base.metadata.create_all(bind=engine)
