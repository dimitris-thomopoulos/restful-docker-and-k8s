from swagger_server.service.student_service import *
import connexion
from swagger_server.models.student import Student

def add_student(body=None):
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json()) 
        return add(body)
    return 500, 'error'
    
def delete_student(student_id):
    return delete(student_id)

def get_student_by_id(student_id):
    return get_by_id(student_id)

def get_average_grade(student_id):
    from swagger_server.service.student_service import get_average_grade as avg_service
    return avg_service(student_id)