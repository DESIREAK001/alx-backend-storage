#!/usr/bin/env python3
""" 100-students.py """


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    The aggregation pipeline calculates the average score for each student
    by using the $avg operator in the $project stage. The pipeline then sorts
    the students by average score in descending order using the $sort stage.
    """
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ])
