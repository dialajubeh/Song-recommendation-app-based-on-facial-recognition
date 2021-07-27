from django import forms
from .models import Message

class FriendsModelForm(forms.ModelForm): #creating a form for profile model
    class Meta:
        model = Message
        fields = ('receiver_msg',)   ## what fields we want to update