from django.shortcuts import render
from spaces.permissions import IsMemberOfSpace, IsTeacherOfSpace
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Collections, Questions
from .serializers import CollectionSerializer, QuestionSerializer, GetCollectionSerializer, GetQuestionSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@permission_classes([IsAuthenticated, IsTeacherOfSpace])
@api_view(["POST"])
def create_collection(request, spaceId):
    if request.method == "POST":
        copied_data = request.data.copy()
        copied_data['spaceId'] = spaceId
        copied_data['created_by'] = request.user.id
        serializer = CollectionSerializer(data = copied_data)
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            response['message'] = f"Collection created successfully by {request.user.username} in {spaceId} space"
            response['created_by'] = request.user.username
            return Response(response, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    return Response(status = status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, IsMemberOfSpace])
@api_view(['GET'])
def get_collections(request, spaceId):
    serializer = GetCollectionSerializer(Collections.objects.filter(spaceId = spaceId), many = True)
    if serializer:
        response = serializer.data
        return Response(response, status = status.HTTP_200_OK)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsAuthenticated, IsMemberOfSpace])
@api_view(['GET'])
def question_list(request, spaceId):
    collectionId = request.query_params.get('collectionId')
    if request.method == 'GET':
        questions = Questions.objects.filter(collectionId = collectionId)
        serializer = GetQuestionSerializer(questions, many = True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, IsTeacherOfSpace])
@api_view(["POST"])
def create_question(request, spaceId):
    '''
    Question Payload:
    
    {
    "collectionId": 1,
    "questions": [
        {
            "question": "What is the capital of France?",
            "option1": "Paris",
            "option2": "London",
            "option3": "Berlin",
            "option4": "Madrid",
            "correct_answer": "Paris"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "option1": "Earth",
            "option2": "Jupiter",
            "option3": "Mars",
            "option4": "Venus",
            "correct_answer": "Jupiter"
        }
    ]
}  
    '''
    if request.method == "POST":
        collectionId = request.data['collectionId']
        question_data = request.data['questions']
        if not collectionId:
            return Response({"detail": "No collectionId provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not question_data:
            return Response({"detail": "No questions data provided."}, status=status.HTTP_400_BAD_REQUEST)
        serializers = []
        for question in question_data:
            question['collectionId'] = collectionId
            serializer = QuestionSerializer(data = question)
            serializers.append(serializer)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            for serializer in serializers:
                serializer.save()
                
        return Response({"detail": "Questions created successfully."}, status=status.HTTP_201_CREATED)
    
@permission_classes([IsAuthenticated, IsMemberOfSpace])
@api_view(['POST'])
def submit_answersheet(request, spaceId):
    '''
    Answersheet Submission Payload:
    {
    "collectionId": 1,
    "questions": [
        {
            "questionId": 1,
            "answer": "Paris"
        },
        {
            "questionId": 2,
            "answer": "Jupiter"
        }
    ]
}  
    '''
    
    if request.method == "POST":
        collectionId = request.data['collectionId']
        question_data = request.data['questions']
        if not collectionId:
            return Response({"message": "No collectionId provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not question_data:
            return Response({"message": "No questions data provided."}, status=status.HTTP_400_BAD_REQUEST)
        # questions = Questions.objects.filter(collectionId = collectionId, many = True)
        marks_per_question = (Collections.objects.get(collectionId = collectionId).marks)/len(Questions.objects.filter(collectionId = collectionId))
        obtained_marks = 0
        chosen_answers = {}
        for items in question_data:
            question = Questions.objects.get(questionId = items['questionId'])
            chosen_answers[question.questionId] = items['answer']
            if question.correct_answer == items['answer']:
                obtained_marks += marks_per_question
    
        serializer = QuestionSerializer(Questions.objects.filter(collectionId = collectionId), many = True)
        response = serializer.data
        for items in response:
            items['chosen_answer'] = chosen_answers[items['questionId']]
            
        pass_fail = "Pass" if obtained_marks >= Collections.objects.get(collectionId = collectionId).pass_marks else "Fail"
        return Response({"message": "Answersheet submitted successfully.", "obtained_marks": obtained_marks, "questions": response, "remark":pass_fail}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
