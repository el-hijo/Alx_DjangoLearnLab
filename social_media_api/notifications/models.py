from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()
# Create your models here.

class Notification(models.Model):
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    actor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="acted_notifications",null=True,blank=True)
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-timestamp"]
        indexes = [models.Index(fields=["recipient", "unread", "timestamp"]),]

    def __str__(self):
        actor = getattr(self.actor, "username", "Someone")
        return f"Notification to {self.recipient} — {actor} {self.verb}"

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save(update_fields=["unread"])