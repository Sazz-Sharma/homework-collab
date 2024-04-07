from django.db import models
import uuid
from datetime import datetime, timedelta
import os
# Create your models here.
def time_plus_days():
    return datetime.now() + timedelta(days=3)

class Portal(models.Model):
    portalId = models.UUIDField(primary_key = False, default = uuid.uuid4, editable = False, unique = True)
    space = models.ForeignKey("spaces.Space", to_field = 'spaceId', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    submission_start = models.DateTimeField(default = datetime.now)
    deadline = models.DateTimeField(default = time_plus_days)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    def __str__(self):
        return self.name

def get_upload_path(instance, filename):
    return os.path.join(
        "portal_submissions", "%d" % instance.portal.space.id, "%d" % instance.portal.id, instance.user.username, filename)

class PortalSubmission(models.Model):
    portalSubmissionId = models.UUIDField(primary_key = False, default = uuid.uuid4, editable = False, unique = True)
    portal = models.ForeignKey(Portal, to_field = 'portalId', on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    # file_path = models.TextField(default= )
    submission = models.FileField(upload_to=get_upload_path)
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.portal.name + " - " + self.user.username
    
    