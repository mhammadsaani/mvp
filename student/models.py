from django.db import models
from django.conf import settings
from django.utils import timezone
from teacher.models import TeacherProfile

class StudentProfile(models.Model):
    """
    Student/Guardian profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    education_level = models.CharField(max_length=100, blank=True, null=True)
    subjects_of_interest = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class JobPost(models.Model):
    """
    Student job post for teacher requirements
    """
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)
    preferred_experience = models.PositiveIntegerField(default=0, help_text="Preferred years of experience")
    budget_range = models.CharField(max_length=100, blank=True, null=True)
    location_preference = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    requirements_met = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Bidding cycle management
    current_bid_cycle = models.PositiveIntegerField(default=1)
    max_bids_current_cycle = models.PositiveIntegerField(default=10)  # 10 for first cycle, +5 for each subsequent cycle
    
    def __str__(self):
        return f"{self.title} - {self.student.user.username}"
    
    @property
    def is_recent(self):
        """Check if job post is less than 5 minutes old"""
        time_diff = timezone.now() - self.created_at
        return time_diff.total_seconds() < 300  # 5 minutes = 300 seconds
    
    def increment_bid_cycle(self):
        """Increment bid cycle and update max bids"""
        self.current_bid_cycle += 1
        self.max_bids_current_cycle += 5  # Add 5 more bids for each cycle
        self.requirements_met = False
        self.save()

class TeacherBid(models.Model):
    """
    Teacher bids on student job posts
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='bids')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='bids')
    proposal = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=255)
    similarity_score = models.FloatField(default=0)  # Calculated based on job requirements and teacher profile
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job_post', 'teacher')
        ordering = ['-similarity_score', 'created_at']
    
    def __str__(self):
        return f"{self.teacher.user.username}'s bid on {self.job_post.title}"

class StudentTeacherContact(models.Model):
    """
    Record of student-teacher contacts
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='teacher_contacts')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='student_contacts')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    message = models.TextField()
    coins_used = models.PositiveIntegerField(default=0)  # 0 if free contact
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contact: {self.student.user.username} - {self.teacher.user.username}"
