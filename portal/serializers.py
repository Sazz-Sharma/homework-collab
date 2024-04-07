from rest_framework import serializers
from .models import Portal, PortalSubmission

class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portal
        fields = '__all__'
        
class PortalSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalSubmission
        fields = '__all__'
        
        