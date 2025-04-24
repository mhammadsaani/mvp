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
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_range': forms.TextInput(attrs={'class': 'form-control'}),
            'location_preference': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudentTeacherContactForm(forms.ModelForm):
    """
    Form for students to contact teachers
    """
    class Meta:
        model = StudentTeacherContact
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }