import os

from pymongo import MongoClient

# Configuration from environment (for Docker/Kubernetes and local docker-compose)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "student_db")
COLLECTION_NAME = "students"

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def _get_collection():
    return _get_client()[MONGO_DB_NAME][COLLECTION_NAME]


def add(student=None):
    if student is None:
        return "invalid input", 400
    coll = _get_collection()
    if coll.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return "already exists", 409
    # Use integer student_id for API compatibility (same as previous TinyDB doc_id)
    cursor = coll.find({}, {"student_id": 1}).sort("student_id", -1).limit(1)
    next_id = 1
    for doc in cursor:
        if doc.get("student_id") is not None:
            next_id = doc["student_id"] + 1
        break
    doc = student.to_dict()
    doc["student_id"] = next_id
    coll.insert_one(doc)
    student.student_id = next_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    if student_id is None:
        return "not found", 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return "not found", 404
    coll = _get_collection()
    student = coll.find_one({"student_id": sid})
    if not student:
        return "not found", 404
    # Remove MongoDB _id for API response; ensure student_id is present
    student["student_id"] = sid
    if "_id" in student:
        del student["_id"]
    return student


def delete(student_id=None):
    if student_id is None:
        return "not found", 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return "not found", 404
    coll = _get_collection()
    result = coll.delete_one({"student_id": sid})
    if result.deleted_count == 0:
        return "not found", 404
    return sid

import os

from pymongo import MongoClient

# Configuration from environment (for Docker/Kubernetes and local docker-compose)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "student_db")
COLLECTION_NAME = "students"

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def _get_collection():
    return _get_client()[MONGO_DB_NAME][COLLECTION_NAME]


def add(student=None):
    if student is None:
        return "invalid input", 400
    coll = _get_collection()
    if coll.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return "already exists", 409
    cursor = coll.find({}, {"student_id": 1}).sort("student_id", -1).limit(1)
    next_id = 1
    for doc in cursor:
        if doc.get("student_id") is not None:
            next_id = doc["student_id"] + 1
        break
    doc = student.to_dict()
    doc["student_id"] = next_id
    coll.insert_one(doc)
    student.student_id = next_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    if student_id is None:
        return "not found", 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return "not found", 404
    coll = _get_collection()
    student = coll.find_one({"student_id": sid})
    if not student:
        return "not found", 404
    student["student_id"] = sid
    if "_id" in student:
        del student["_id"]
    return student


def delete(student_id=None):
    if student_id is None:
        return "not found", 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return "not found", 404
    coll = _get_collection()
    result = coll.delete_one({"student_id": sid})
    if result.deleted_count == 0:
        return "not found", 404
    return sid


def get_average_grade(student_id=None):
    if student_id is None:
        return "not found", 404
    try:
        sid = int(student_id)
    except (TypeError, ValueError):
        return "not found", 404
    coll = _get_collection()
    student = coll.find_one({"student_id": sid})
    if not student:
        return "not found", 404
    grade_records = student.get("grade_records")
    if not grade_records:
        return "not found", 404
    average = sum(r["grade"] for r in grade_records) / len(grade_records)
    return round(average, 2)