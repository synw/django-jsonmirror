from __future__ import print_function
from rethinkdb import r
from djR.r_producers import R
from jsonmirror.conf import BACKEND, DB, TABLE
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
    q = r.db(DB).table(table).filter({"pk":pk, "model":modelname}).order_by("timestamp").pluck("pk","model")
    existing_documents = R.run_query(q)
    json_document_exists = False
    if len(existing_documents) > 0:
        json_document_exists = True
    return json_document_exists


def delete_model(instance):
    modelname = str(instance._meta)
    soft_delete = get_option(instance, "soft_delete")
    if soft_delete is False:
        document_exists_in_db = document_exists(DB, TABLE, modelname, instance.pk)
        if document_exists_in_db:
            filters = {"model": modelname, "pk": instance.pk}
            R.delete_filtered(DB, TABLE, filters)
    return


def mirror_model(instance, data, created=False, verbose=False, table=None):
    res = {"created": 0, "updated": 0}
    modelname = str(instance._meta)
    table_to_use = TABLE
    if table is not None:
        table_to_use = table
    # record data
    if created is True:
        res["status"] = R.write(DB, table_to_use, data)
        res["created"] += 1
        if verbose is True:
            print("[ "+modelname+" ] Document "+str(instance.pk)+" created in table "+table_to_use)
    else:
        optype = "write"
        imutable = get_option(instance, "imutable")
        if imutable is False:
            document_exists_in_db = document_exists(DB, table_to_use, modelname, instance.pk)
            if document_exists_in_db:
                optype = "update"
        if optype == "update":
            res["status"] = R.update(DB, table_to_use, data,{})
            res["updated"] += 1
            if verbose is True:
                print("[ "+modelname+" ] Document "+str(instance.pk)+" updated in table "+table_to_use)
            return res
        res["status"] = R.write(DB, table_to_use, data)
        res["created"] += 1
        if verbose is True:
            print("[ "+modelname+" ] Document "+str(instance.pk)+" created in table "+table_to_use)
    return res
