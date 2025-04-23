from django import forms
from .models import JobPost, StudentTeacherContact

class JobPostForm(forms.ModelForm):
    """
    Form for creating and editing job posts
    """
    class Meta:
        model = JobPost
        fields = ['title', 'subject', 'description', 'education_level', 'preferred_experience', 'budget_range', 'location_preference']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class StudentTeacherContactForm(forms.ModelForm):
    """
    Form for students to contact teachers
    """
    class Meta:
        model = StudentTeacherContact
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }