from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_username_from_id(request):
    userId = request.query_params.get('userId')
    if request.method == "GET":
        user = User.objects.get(pk = userId)
        return Response({'username': user.username}, status = status.HTTP_200_OK)
