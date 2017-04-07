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


def delete_model(instance, verbose=True):
    soft_delete = get_option(instance, "soft_delete")
    imutable = get_option(instance, "imutable")
    if soft_delete is True:
        return
    if imutable is True:
        raise ImproperlyConfigured("Whith sqlite it is not possible to use soft_delete and imutability together")
    rec = session.query(Mirror).get(instance.id)
    session.query(Mirror).delete(id=rec.id)
    return rec
    
def mirror_model(instance, data, created, verbose=True, table="mirror"):
    data = json.dumps(data)
    imutable = get_option(instance, "imutable")
    soft_delete = get_option(instance, "soft_delete")
    key = instance.id
    if imutable == True or soft_delete is True:
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
