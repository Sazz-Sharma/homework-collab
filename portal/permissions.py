from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from .models import UserSpace

def IsStudentOfSpace(BasePermission):
    def has_permission(self, request, view):
        try:
            spaceId = request.resolver_match.kwargs.get('spaceId')
            token = request.headers['Authorization'].split()[1]
            student_id = Token.objects.get(key = token).user_id
            specific_user_space = UserSpace.objects.get(user = student_id, space = spaceId)
            return not specific_user_space.is_teacher
        except:
            return False
