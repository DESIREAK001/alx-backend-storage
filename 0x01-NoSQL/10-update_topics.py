#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the name.

    Parameters
    ----------
    mongo_collection : pymongo.collection.Collection
        MongoDB collection object
    name : str
        The name of the school to update the topics for
    topics : list
        The new list of topics for the school
    """
    mongo_collection.update_many(
        {"name": name},  # filter the documents to update
        {"$set": {"topics": topics}},  # update the topics field with the new topics
    )
