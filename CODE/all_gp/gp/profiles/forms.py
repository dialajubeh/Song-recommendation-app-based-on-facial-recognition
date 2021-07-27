from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm): #creating a form for profile model
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio','email','country',)   ## what fields we want to update