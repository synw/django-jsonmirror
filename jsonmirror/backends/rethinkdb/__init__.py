from __future__ import print_function
from rethinkdb import r
from djR.r_producers import R
from jsonmirror.conf import get_option


def order_documents(docs):
    ordered_docs = {}
    for doc in docs:       
        if doc["model"] in ordered_docs.keys():
            ordered_docs[doc["model"]] = ordered_docs[doc["model"]].append(doc["pk"])
        else:
            ordered_docs[doc["model"]] = [doc["pk"]]
    return ordered_docs


def document_exists(db, table, modelname, pk):
    q = r.db(db).table(table).filter({"pk":pk, "model":modelname}).order_by("timestamp").pluck("pk","model")
    existing_documents = R.run_query(q)
    json_document_exists = False
    if len(existing_documents) > 0:
        json_document_exists = True
        return json_document_exists, existing_documents[0]
    return json_document_exists, None


def delete_model(instance, db, table, imutable, soft_delete):
    modelname = str(instance._meta)
    if imutable == True:
        soft_delete = True
    filters = {"model": modelname, "pk": instance.pk}
    document_exists_in_db, document = document_exists(db, table, modelname, instance.pk)
    if soft_delete is False:
        if document_exists_in_db:
            R.delete_filtered(db, table, filters)
    else:
        document["deleted"] = True
        R.update(db, table, document, filters)
    return


def mirror_model(instance, data, db, table, created, imutable, verbose=False):
    res = {"created": 0, "updated": 0}
    modelname = str(instance._meta)
    # record data
    if created is True:
        res["status"] = R.write(db, table, data)
        res["created"] += 1
        if verbose is True:
            print("[ "+modelname+" ] Document "+str(instance.pk)+" created in table "+table)
    else:
        optype = "write"
        if imutable is False:
            document_exists_in_db, document = document_exists(db, table, modelname, instance.pk)
            if document_exists_in_db:
                optype = "update"
        if optype == "update":
            res["status"] = R.update(db, table, data,{})
            res["updated"] += 1
            if verbose is True:
                print("[ "+modelname+" ] Document "+str(instance.pk)+" updated in table "+table)
            return res
        res["status"] = R.write(db, table, data)
        res["created"] += 1
        if verbose is True:
            print("[ "+modelname+" ] Document "+str(instance.pk)+" created in table "+table)
    return res
