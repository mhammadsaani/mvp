from django.db import models
from django.conf import settings
from django.utils import timezone

class TeacherProfile(models.Model):
    """
    Teacher profile with detailed information
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True, null=True)
    expertise = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    education = models.TextField(blank=True, null=True)
    coins = models.PositiveIntegerField(default=0)
    similarity_score = models.FloatField(default=0)  # Used for job matching
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Certification(models.Model):
    """
    Teacher certifications
    """
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/')
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.teacher.user.username}"
    
    @property
    def is_valid(self):
        if not self.expiry_date:
            return True
        return self.expiry_date >= timezone.now().date()

class TeacherTimetable(models.Model):
    """
    Teacher timetable for classes
    """
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='timetables')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    number_of_classes = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    days_available = models.CharField(max_length=255, help_text="Comma-separated days, e.g., 'Monday,Wednesday,Friday'")
    time_slots = models.CharField(max_length=255, help_text="Comma-separated time slots, e.g., '9:00-10:00,14:00-15:00'")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.teacher.user.username}"

class CoinTransaction(models.Model):
    """
    Record of coin purchases and usage
    """
    TRANSACTION_TYPE_CHOICES = (
        ('purchase', 'Purchase'),
        ('usage', 'Usage'),
        ('refund', 'Refund'),
    )
    
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='coin_transactions')
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} coins - {self.teacher.user.username}"
