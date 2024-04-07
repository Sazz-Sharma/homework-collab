from rest_framework.permissions import BasePermission
from .models import UserSpace
from rest_framework.authtoken.models import Token
from rest_framework import permissions

# class IsTeacherOfSpace(BasePermission):
#     def is_teacher(self, request, view, obj):
#         return obj.teacher == request.user

class IsTeacherOfSpace(BasePermission):
    def has_permission(self, request, view):
        # user_space = UserSpace.objects.get(user = request.user, space = request.data['spaceId'])
        # return user_space.is_teacher
        # print(request.user.)
        try:
            spaceId = request.resolver_match.kwargs.get('spaceId')
            # print(request)
            # space = UserSpace.objects.get(space = spaceId)
            # token = request.headers['Authorization'].split()[1]
            
            teacher_id = request.user.id   
            specific_user_space = UserSpace.objects.get(user = teacher_id, space = spaceId)
            print(specific_user_space.is_teacher)
            return specific_user_space.is_teacher
        except:
            return False
       
        
        
class IsTeacherOfSpaceOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            spaceId = request.resolver_match.kwargs.get('spaceId')
            token = request.headers['Authorization'].split()[1]
            teacher_id = Token.objects.get(key = token).user_id
            specific_user_space = UserSpace.objects.get(user = teacher_id, space = spaceId)
            return specific_user_space.is_teacher
        except:
            return False

        
