#!/usr/bin/env python3
""" 12-log_stats """
from pymongo import MongoClient


def main():
    """
    Main function that connects to the MongoDB logs database,
    retrieves the number of logs per method and prints the results.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    # Count the number of GET, POST, PUT, PATCH and DELETE requests
    get = logs_collection.count_documents({'method': 'GET'})
    post = logs_collection.count_documents({'method': 'POST'})
    put = logs_collection.count_documents({'method': 'PUT'})
    patch = logs_collection.count_documents({'method': 'PATCH'})
    delete = logs_collection.count_documents({'method': 'DELETE'})

    # Count the number of GET requests to /status
    st = logs_collection.count_documents({'method': 'GET', 'path': '/status'})

    # Print the number of logs, methods and status checks
    print('{} logs'.format(logs_collection.count_documents({})))
    print('Methods:')
    print('\tmethod GET: {}'.format(get))
    print('\tmethod POST: {}'.format(post))
    print('\tmethod PUT: {}'.format(put))
    print('\tmethod PATCH: {}'.format(patch))
    print('\tmethod DELETE: {}'.format(delete))
    print('{} status check'.format(st))


if __name__ == "__main__":
    main()
