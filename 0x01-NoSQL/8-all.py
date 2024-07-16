#!/usr/bin/env python3
""" 8-all """


def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Parameters
    ----------
    mongo_collection : pymongo.collection.Collection
        MongoDB collection object

    Returns
    -------
    cursor
        A cursor to the documents in the collection
    """
    return mongo_collection.find({})
