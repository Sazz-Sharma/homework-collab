from rest_framework import serializers
from .models import Space, UserSpace, Notice, JoinRequest
from django.contrib.auth.models import User


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'
class UserSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpace
        fields = '__all__'
        
class GetUserSpaceSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserSpace
        fields = ('user_username', 'is_teacher')
        
class GetSpaceSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField(source='teacher.username', read_only=True)
    class Meta:
        model = Space
        fields = ('spaceId', 'name', 'teacher_username', 'created_at')
        
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        
class GetNoticeSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(source='created_by.username', read_only=True)
    creator_name = serializers.CharField(source='created_by.username', read_only=True)
    space_name = serializers.CharField(source='space.name', read_only=True)
    
    class Meta:
        model = Notice
        fields = ('noticeId', 'space_name', 'title', 'content', 'created_at', 'deadline', 'creator_name')
        
class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = '__all__'
