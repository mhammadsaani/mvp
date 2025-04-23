from django import forms
from .models import TeacherProfile, Certification, TeacherTimetable, CoinTransaction
from student.models import TeacherBid

class TeacherProfileForm(forms.ModelForm):
    """
    Form for creating and editing teacher profiles
    """
    class Meta:
        model = TeacherProfile
        fields = ['expertise', 'experience_years', 'education', 'hourly_rate', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class CertificationForm(forms.ModelForm):
    """
    Form for adding and editing certifications
    """
    class Meta:
        model = Certification
        fields = ['title', 'issuing_organization', 'issue_date', 'expiry_date', 'certificate_file']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TeacherTimetableForm(forms.ModelForm):
    """
    Form for creating and editing timetables
    """
    class Meta:
        model = TeacherTimetable
        fields = ['title', 'days_available', 'time_slots', 'number_of_classes', 'hourly_rate', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BidForm(forms.ModelForm):
    """
    Form for creating and editing bids
    """
    class Meta:
        model = TeacherBid
        fields = ['hourly_rate', 'proposal', 'availability']
        widgets = {
            'proposal': forms.Textarea(attrs={'rows': 5}),
        }

class CoinPurchaseForm(forms.Form):
    """
    Form for purchasing coins
    """
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    coins_amount = forms.IntegerField(min_value=10, max_value=1000, label='Number of Coins')
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Payment Method')