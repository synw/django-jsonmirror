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
    modelname = Column(String)
    
    def __repr__(self):
        return "<Mirror(id: '%s', data: '%s'')>" % (self.id, self.data)


def delete_model(instance, dbname, table, imutable, soft_delete):
    if imutable is True:
        return
    modelname = instance.__class__.__name__
    rec = session.query(Mirror).filter_by(id=instance.id, modelname=modelname).first()
    if soft_delete is True:
        data = json.loads(rec.data)
        data["deleted"] = True
        data = json.dumps(data)
        rec.data = data
        session.add(rec)
    else:
        session.delete(rec)
    session.commit()
    return
    
def mirror_model(instance, data, db, table, created, imutable):
    data = json.dumps(data)
    num = session.query(Mirror).count()
    key = num+1
    modelname = instance.__class__.__name__
    obj = Mirror(key=key, id=instance.id, data=data, modelname=instance.__class__.__name__)
    if created is True:
        session.add(obj)
    else:
        if imutable is False:
            rec = session.query(Mirror).filter_by(id=instance.id, modelname=modelname).first()
            if rec:
                rec.data = data
                session.add(rec)
            else:
                session.add(obj)
        else:
            session.add(obj)
    session.commit()
    return

Base.metadata.create_all(engine, checkfirst=True)
