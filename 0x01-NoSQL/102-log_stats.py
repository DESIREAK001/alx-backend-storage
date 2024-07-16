#!/usr/bin/env python3
""" 102-log_stats """
from pymongo import MongoClient


def main():
    """
    Main function that connects to the MongoDB logs database,
    retrieves some statistics and prints the results.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    # Count the number of logs
    total_logs = logs_collection.count_documents({})
    print('{} logs'.format(total_logs))

    # Count the number of requests per method
    get = logs_collection.count_documents({'method': 'GET'})
    post = logs_collection.count_documents({'method': 'POST'})
    put = logs_collection.count_documents({'method': 'PUT'})
    patch = logs_collection.count_documents({'method': 'PATCH'})
    delete = logs_collection.count_documents({'method': 'DELETE'})

    # Print the number of logs per method
    print('Methods:')
    print('\tmethod GET: {}'.format(get))
    print('\tmethod POST: {}'.format(post))
    print('\tmethod PUT: {}'.format(put))
    print('\tmethod PATCH: {}'.format(patch))
    print('\tmethod DELETE: {}'.format(delete))

    # Count the number of GET requests to /status
    st = logs_collection.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(st))

    # Retrieve the top 10 IPs with the most requests
    IPs = logs_collection.aggregate([
        {"$group": {
            "_id": "$ip",
            "total": {"$sum": 1}
        }}, {
            "$sort": {
                "total": -1
            }
        }, {
            "$limit": 10
        }
    ])

    # Print the top 10 IPs with the most requests
    print('IPs:')
    for ip in IPs:
        print('\t{}: {}'.format(ip.get('_id'), ip.get('total')))


if __name__ == "__main__":
    main()
