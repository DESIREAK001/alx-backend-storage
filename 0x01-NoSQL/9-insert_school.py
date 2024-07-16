#!/usr/bin/env python3
""" 9-insert_school """


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection.

    Parameters
    ----------
    mongo_collection : pymongo.collection.Collection
        MongoDB collection object
    kwargs : dict
        The document to insert, represented as a dictionary

    Returns
    -------
    ObjectId
        The ID of the inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id
