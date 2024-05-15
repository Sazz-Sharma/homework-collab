from django.db import models
from datetime import datetime, timedelta
from spaces.models import Space
# from spaces.models import Space
def time_plus_days():
    return datetime.now() + timedelta(days=3)

# Create your models here.
class Collections(models.Model):
    collectionId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None, null= True)
    spaceId = models.ForeignKey("spaces.Space",to_field="spaceId", on_delete=models.CASCADE)
    marks = models.IntegerField()
    pass_marks = models.IntegerField(default=0)
    time_in_minutes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default = time_plus_days)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.pass_marks == 0 and self.marks is not None:
            self.pass_marks = int(0.4 * self.marks)
        super(Collections, self).save(*args, **kwargs)
    
class Questions(models.Model):
    questionId = models.AutoField(primary_key=True)
    collectionId = models.ForeignKey(Collections, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.TextField(default=None)
    option2 = models.TextField(default=None)
    option3 = models.TextField(default = None)
    option4 = models.TextField(default=None)
    correct_answer = models.TextField(default=None)
    
    
    