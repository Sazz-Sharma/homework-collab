from rest_framework import serializers
from .models import Collections, Questions

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = '__all__'
class GetCollectionSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    spaceId = serializers.CharField(source='spaceId.name', read_only=True)
    class Meta:
        model = Collections
        fields = '__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'questionId': representation['questionId'],
            'collectionId': representation['collectionId'],
            'question': representation['question'],
            'options': {
                'option1': representation['option1'],
                'option2': representation['option2'],
                'option3': representation['option3'],
                'option4': representation['option4'],
            },
            'correct_answer': representation['correct_answer']
        }
        
class GetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'questionId': representation['questionId'],
            'collectionId': representation['collectionId'],
            'question': representation['question'],
            'options': {
                'option1': representation['option1'],
                'option2': representation['option2'],
                'option3': representation['option3'],
                'option4': representation['option4'],
            },
        }

