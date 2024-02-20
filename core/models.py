from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Notes(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User,related_name='note_owner',on_delete=models.CASCADE)
    shared = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text + "by" + self.owner.username
    
class NotesVersionHistory(models.Model):
    notes = models.ForeignKey(Notes,on_delete=models.CASCADE)
    action_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='crd_by',on_delete=models.CASCADE,null=True)
    updated_by = models.ForeignKey(User,related_name='upd_by',on_delete=models.CASCADE,null=True)
    created = models.BooleanField(null=True)
    updated = models.BooleanField(null=True)