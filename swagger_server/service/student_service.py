# coding: utf-8
"""Student service using MongoDB."""
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from swagger_server.config import MONGO_URI, MONGO_DB_NAME

_COLLECTION = "students"

_client = MongoClient(MONGO_URI)
_db = _client[MONGO_DB_NAME]
student_collection = _db[_COLLECTION]


def add(student=None):
    if student is None:
        return 'invalid', 400
    doc = student.to_dict()
    # Remove student_id for insert; we use _id as the numeric id
    doc.pop('student_id', None)
    # Get next id: max(_id) + 1
    cursor = student_collection.find({}).sort("_id", -1).limit(1)
    next_id = 1
    for d in cursor:
        next_id = d["_id"] + 1
        break
    doc["_id"] = next_id
    # Check duplicate by first_name + last_name
    if student_collection.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return 'already exists', 409
    try:
        student_collection.insert_one(doc)
    except DuplicateKeyError:
        return 'already exists', 409
    student.student_id = next_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    if student_id is None:
        return 'not found', 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return 'not found', 404
    student = student_collection.find_one({"_id": sid})
    if not student:
        return 'not found', 404
    # Return dict with student_id (API expects student_id, not _id in response)
    student["student_id"] = student.pop("_id")
    return student


def delete(student_id=None):
    if student_id is None:
        return 'not found', 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return 'not found', 404
    result = student_collection.delete_one({"_id": sid})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id
