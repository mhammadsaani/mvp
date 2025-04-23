from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from .models import SystemConfiguration

class TeacherCreationForm(UserCreationForm):
    """
    Form for admin to create teacher accounts
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'address', 'profile_picture', 'password1', 'password2']

class SystemConfigForm(forms.ModelForm):
    """
    Form for managing system configuration
    """
    class Meta:
        model = SystemConfiguration
        fields = ['key', 'value', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }