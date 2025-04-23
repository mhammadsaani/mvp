from django.db import models
from django.conf import settings
from django.utils import timezone

class AdminAction(models.Model):
    """
    Record of admin actions for auditing purposes
    """
    ACTION_TYPE_CHOICES = (
        ('block_user', 'Block User'),
        ('unblock_user', 'Unblock User'),
        ('remove_post', 'Remove Job Post'),
        ('remove_teacher', 'Remove Teacher Profile'),
        ('verify_certification', 'Verify Certification'),
        ('other', 'Other Action'),
    )
    
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   related_name='admin_actions_received', null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action_type} by {self.admin.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class SystemConfiguration(models.Model):
    """
    System-wide configuration settings
    """
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.key
    
    @classmethod
    def get_value(cls, key, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default
