from swagger_server.service.student_service import *
import connexion
# Import the Student model so the controller can use it
from swagger_server.models.student import Student 

def add_student(body=None):
    """Add a new student..."""
    if connexion.request.is_json:
        # Now 'Student' is defined and this will work
        body = Student.from_dict(connexion.request.get_json()) 
        return add(body)
    return 500, 'error'

def delete_student(student_id):  # noqa: E501
    """deletes a student

    delete a single student  # noqa: E501

    :param student_id: the uid
    :type student_id: int

    :rtype: None
    """
    return delete(student_id)


def get_student_by_id(student_id):  # noqa: E501
    """gets student

    Returns a single student # noqa: E501

    :param student_id: the uid
    :type student_id: int

    :rtype: Student
    """
    return get_by_id(student_id)
