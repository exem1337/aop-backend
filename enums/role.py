from enum import Enum


class ERole(Enum):
    STUDENT = 'student'
    EXPERT = 'expert'
    OPERATOR = 'operator'


available_roles = [role.value for role in ERole]
