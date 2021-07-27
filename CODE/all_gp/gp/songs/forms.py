from django import forms
from .models import Playlist,Song
import django_tables2 as tables


class PlaylistModelForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('list_name', 'list',)   ## what fields we want to update

class SongModelForm(forms.Form):
    form = forms.ModelChoiceField(queryset=Song.objects.all())
