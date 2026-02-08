# coding: utf-8
"""Configuration for database and application (from environment)."""
import os

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "student_db")
