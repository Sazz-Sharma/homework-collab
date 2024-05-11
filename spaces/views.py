from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SpaceSerializer, UserSpaceSerializer, GetSpaceSerializer, GetNoticeSerializer, NoticeSerializer, JoinRequestSerializer, GetUserSpaceSerializer
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .permissions import IsTeacherOfSpace, IsTeacherOfSpaceOrReadOnly
from .models import Space, UserSpace, Notice, JoinRequest
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_space(request):
    if request.method == "POST":
        copied_data = request.data.copy()
        copied_data['teacher'] = request.user.id
        serializer = SpaceSerializer(data=copied_data)
        # token = request.headers['Authorization'].split()[1]
        # teacher_id = Token.objects.get(key = token).user_id
        if serializer.is_valid():
            # serializer.validated_data['teacher'] = User.objects.get(pk = teacher_id)
            serializer.save()
            userspaceserializer = UserSpaceSerializer(data = {'user': User.objects.get(pk = copied_data['teacher']).id, 'space': serializer.data['spaceId'], 'is_teacher': True})
            if userspaceserializer.is_valid():
                userspaceserializer.save()
            message = f" {serializer.data['name']} created by {User.objects.get(pk = serializer.data['teacher']).username} successfully"
            # Process the validated data
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsTeacherOfSpace])
def add_member(request, spaceId, member_name):
    try:
        space = Space.objects.get(spaceId=spaceId)
        member_name = User.objects.get(username=member_name)
    except Space.DoesNotExist:
        return Response({'error': 'Space does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        if UserSpace.objects.filter(user = member_name.id, space = spaceId).exists():
            return Response({'error': 'User already exists in the space.'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data 
        copied_data = data.copy()
        copied_data['space'] = spaceId
        copied_data['user'] = member_name.id
        serializer = UserSpaceSerializer(data=copied_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method=="DELETE":
        if UserSpace.objects.filter(user = member_name.id, space = spaceId).exists():
            UserSpace.objects.filter(user = member_name.id, space = spaceId).delete()
            return Response({'message': 'User removed from space'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User does not exist in the space'}, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({'error': 'User does not exist in the space'}, status=status.HTTP_400_BAD_REQUEST)   

@api_view(['PATCH']) 
@permission_classes([IsAuthenticated, IsTeacherOfSpace])
def change_to_teacher(request, spaceId, member_name):
    try:
        space = Space.objects.get(spaceId=spaceId)
        member_name = User.objects.get(username=member_name)
    except Space.DoesNotExist:
        return Response({'error': 'Space does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "PATCH":
        if UserSpace.objects.filter(user = member_name.id, space = spaceId).exists():
            UserSpace.objects.filter(user = member_name.id, space = spaceId).update(is_teacher = True)
            return Response({'message': 'User is now a teacher'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User does not exist in the space'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spaces(request):
    if request.method == "GET":
        serializer = GetSpaceSerializer(Space.objects.all(), many = True)
        (print(serializer.data))
        # latest_notice = 
        # number_of_members = 
        # number_of_portals = 
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_spaces(request):
    if request.method == "GET":
        # copied_data = request.data.copy()
        
        token = request.headers['Authorization'].split()[1]
        teacher_id = Token.objects.get(key = token).user_id
        user_space_serializer = UserSpaceSerializer(UserSpace.objects.filter(user = teacher_id), many = True)
        
        serializer = GetSpaceSerializer(Space.objects.filter(spaceId__in = [user_space['space'] for user_space in user_space_serializer.data]), many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)   
        
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsTeacherOfSpaceOrReadOnly])
def notice_manager(request, spaceId):
    if request.method == 'POST':
        copied_data = request.data.copy()
        copied_data['space'] = spaceId
        token = request.headers['Authorization'].split()[1]
        teacher_id = Token.objects.get(key = token).user_id
        copied_data['created_by'] = User.objects.get(pk = teacher_id).id
        serializer = NoticeSerializer(data=copied_data)
        if serializer.is_valid():
            # serializer.validated_data['space'] = Space.objects.get(spaceId = spaceId)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        # serializer = GetNoticeSerializer(Notice.objects.filter(space = spaceId, deadline__lt = datetime.now), many = True)
        serializer = GetNoticeSerializer(Notice.objects.filter(space = spaceId), many = True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # if request.method == 'PATCH':
    #     notice = Notice.objects.get(noticeId = request.data['noticeId'])
    #     serializer = NoticeSerializer(notice, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_of_space(request, spaceId):
    if request.method == 'GET':
        user_space_serializer = GetUserSpaceSerializer(UserSpace.objects.filter(space = spaceId), many = True)
        return Response(user_space_serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_join_request(request, spaceId):
    if request.method == 'POST':
        copied_data = request.data.copy()
        copied_data['space'] = spaceId
        token = request.headers['Authorization'].split()[1]
        student_id = Token.objects.get(key = token).user_id
        copied_data['user'] = student_id
        serializer = JoinRequestSerializer(data=copied_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsTeacherOfSpace])
def join_request_manager(request, spaceId):
    if request.method == "GET":
        join_requests = JoinRequest.objects.filter(space = spaceId, is_pending = True)
        return Response(JoinRequestSerializer(join_requests, many = True).data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        join_requests = JoinRequest.objects.get(request_id = request.data['request_id'])
        print(join_requests)
        # request_serializer = 
        
    #     if not(join_requests.get('is_pending', True)):
    #         # join_requests.get('is_pending', False)
    #         join_requests.is_pending = False
    #         user_space_serializer = UserSpaceSerializer(data = {'user': join_requests.user.id, 'space': join_requests.space.spaceId, 'is_teacher': False})
    #         if user_space_serializer.is_valid():
    #             user_space_serializer.save()
    #         join_requests.save()
    #         return Response({'message': 'Request Accepted'}, status=status.HTTP_200_OK) 
    # if request.method == "DELETE":
    #     join_requests.delete()
    #     return Response({'message': 'Request Rejected'}, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsTeacherOfSpace])
def hi(request, spaceId):
    return Response({'message': 'This is teacher'}, status=status.HTTP_200_OK)


