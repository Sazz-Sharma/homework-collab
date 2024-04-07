from django.shortcuts import render

# Create your views here.
# from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .models import Portal, PortalSubmission
from spaces.permissions import IsTeacherOfSpaceOrReadOnly, IsTeacherOfSpace
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Portal, PortalSubmission
from .serializers import PortalSerializer, PortalSubmissionSerializer
from spaces.models import Space
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


@permission_classes([IsTeacherOfSpaceOrReadOnly, IsAuthenticated])
@api_view(['POST', 'GET'])
def create_portal(request, spaceId):
    space = Space.objects.get(spaceId = spaceId)
    if request.method == "POST":
        copied_data = request.data.copy()
        copied_data['space'] = space.spaceId
        token = request.headers['Authorization'].split()[1]
        teacher_id = Token.objects.get(key = token).user_id  
        copied_data['created_by'] = User.objects.get(pk = teacher_id).id
        serializer = PortalSerializer(data=copied_data)
        if serializer.is_valid():
            serializer.save()
            message = f" {serializer.data['name']} created by {request.user.username} successfully"
            
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        portals = Portal.objects.filter(space = space)
        serializer = PortalSerializer(portals, many=True)
        return Response(serializer.data)
    
# @api_view(['GET'])
# def get_portals(request, spaceId):
#     if request.method == "GET":
#         space = Space.objects.get(spaceId = spaceId)
#         portals = Portal.objects.filter(space = space)
#         serializer = PortalSerializer(portals, many=True)
#         return Response(serializer.data)
        
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def submit_portal(request, spaceId, portalId):
    portal = Portal.objects.get(portalId = portalId) 
    if request.method == "POST":
        copied_data = request.data.copy()
        copied_data['portal'] = portalId
        copied_data['user'] = request.user.id
        serializer = PortalSubmissionSerializer(data=copied_data)
        print("Portal Deadline: ", portal.deadline)
        print("Submitted at: ", timezone.now())
        if timezone.now() < portal.deadline:
            if serializer.is_valid():
                serializer.save()
                message = f" {portal.name} submitted by {request.user.username} successfully"
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Submission deadline crossed'}, status=status.HTTP_400_BAD_REQUEST)

