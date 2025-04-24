from django import forms
from .models import JobPost, StudentTeacherContact

class JobPostForm(forms.ModelForm):
    """
    Form for creating and editing job posts
    """
    # Add fields that are in the template but not in the model
    grade_level = forms.ChoiceField(
        choices=[
            ('elementary', 'Elementary School'),
            ('middle', 'Middle School'),
            ('high', 'High School'),
            ('college', 'College/University'),
            ('adult', 'Adult Education')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    teaching_mode = forms.ChoiceField(
        choices=[
            ('in_person', 'In-Person'),
            ('online', 'Online'),
            ('hybrid', 'Hybrid')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    duration = forms.ChoiceField(
        choices=[
            ('one_time', 'One-time Session'),
            ('short_term', 'Short-term (1-4 weeks)'),
            ('medium_term', 'Medium-term (1-3 months)'),
            ('long_term', 'Long-term (3+ months)')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    schedule_preferences = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    additional_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Map model fields to template fields
        if self.instance.pk:
            # Set initial values from the model instance if it exists
            self.fields['grade_level'].initial = self.instance.education_level
            self.fields['location'].initial = self.instance.location_preference
            
            # Additional fields can be stored in the description or as JSON in a future field
            # For now, we'll leave them empty or could parse from description if needed
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Map template fields to model fields
        instance.education_level = self.cleaned_data.get('grade_level')
        instance.location_preference = self.cleaned_data.get('location')
        
        # Store additional fields in the description for now
        # In a future update, these could be stored in a separate JSON field
        additional_info = {
            'teaching_mode': self.cleaned_data.get('teaching_mode'),
            'duration': self.cleaned_data.get('duration'),
            'schedule_preferences': self.cleaned_data.get('schedule_preferences'),
            'additional_requirements': self.cleaned_data.get('additional_requirements')
        }
        
        # Append additional info to description
        if instance.description:
            instance.description += f"\n\nAdditional Information:\n"
        else:
            instance.description = "Additional Information:\n"
            
        for key, value in additional_info.items():
            if value:  # Only add non-empty values
                formatted_key = key.replace('_', ' ').title()
                instance.description += f"- {formatted_key}: {value}\n"
        
        if commit:
            instance.save()
        return instance

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