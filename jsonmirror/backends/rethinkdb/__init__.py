# -*- coding: utf-8 -*-

from rethinkdb import r
from djR.r_producers import R
from jsonmirror.conf import BACKEND, DB, TABLE


def order_documents(docs):
    ordered_docs = {}
    for doc in docs:       
        if doc["model"] in ordered_docs.keys():
            ordered_docs[doc["model"]] = ordered_docs[doc["model"]].append(doc["pk"])
        else:
            ordered_docs[doc["model"]] = [doc["pk"]]
    return ordered_docs


def document_exists(db, table, modelname, pk):
    q = r.db(DB).table(TABLE).filter({"pk":pk, "model":modelname}).order_by("timestamp").pluck("pk","model")
    #existing_documents = order_documents(R.run_query(q))
    #print modelname+" | "+str(pk)+" _> "+str(existing_documents)
    existing_documents = R.run_query(q)
    json_document_exists = False
    if len(existing_documents) > 0:
        json_document_exists = True
    return json_document_exists


def mirror_model(instance, data, created=False, verbose=False):
    res = {"created": 0, "updated": 0}
    modelname = str(instance._meta)
    # record data
    if created is True:
        R.write(DB, TABLE, data)
        res["created"] += 1
        if verbose is True:
            print "[ "+modelname+" ] Document "+str(instance.pk)+" created"
    else:
        # check if the document exists or not
        document_exists_in_db = document_exists(DB, TABLE, modelname, instance.pk)
        if not document_exists_in_db:
            R.write(DB, TABLE, data)
            res["created"] += 1
            if verbose is True:
                print "[ "+modelname+" ] Document "+str(instance.pk)+" created"
        else:
            R.update(DB, TABLE, data, modelname, instance.pk)
            res["updated"] += 1
            if verbose is True:
                print "[ "+modelname+" ] Document "+str(instance.pk)+" updated"
    return res
