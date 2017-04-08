from __future__ import print_function
import json
from django.core.exceptions import ImproperlyConfigured
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from jsonmirror.conf import get_option


engine = create_engine('sqlite:///mirror.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Mirror(Base):
    __tablename__ = 'mirror'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer)
    data = Column(String)
    
    def __repr__(self):
        return "<Mirror(id: '%s', data: '%s'')>" % (self.id, self.data)


def delete_model(instance, dbname, table, imutable, soft_delete):
    if soft_delete is True or imutable is True:
        return
    rec = session.query(Mirror).get(instance.id)
    session.query(Mirror).delete(id=rec.id)
    return rec
    
def mirror_model(instance, data, db, table, created, imutable):
    data = json.dumps(data)
    key = instance.id
    if imutable == True:
        num = session.query(Mirror).count()
        key = num+1
    obj = Mirror(key=key, id=instance.id, data=data)
    if created is True:
        session.add(obj)
    else:
        if imutable is False:
            rec = session.query(Mirror).get(instance.id)
            if rec:
                rec.data = data
            else:
                session.add(obj)
        else:
            session.add(obj)
    session.commit()
    return

Base.metadata.create_all(engine, checkfirst=True)
