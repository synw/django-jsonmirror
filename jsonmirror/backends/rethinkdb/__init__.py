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
    q = r.db(DB).table(TABLE).filter({"pk":pk, "model":modelname}).order_by("model").pluck("pk","model")
    existing_documents = order_documents(R.run_query(q))
    json_document_exists = False 
    if modelname in existing_documents.keys():
        for pk_json in existing_documents[modelname]:
            if pk_json == pk:
                json_document_exists = True
                break
    return json_document_exists
