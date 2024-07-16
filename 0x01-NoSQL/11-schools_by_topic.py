#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Parameters
    ----------
    mongo_collection : pymongo.collection.Collection
        MongoDB collection object
    topic : str
        The topic to search for in the schools' topics list

    Returns
    -------
    list
        List of schools having the topic
    """
    return mongo_collection.find({"topics": topic})
