from django import forms
from .models import Project, UserStory


class UserStoryForm(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = ['project', 'key', 'role', 'actn', 'benefit']
        widgets = {
            'key': forms.TextInput(attrs={
                'id': 'key',
                'class': 'form-control',
                'type': 'number',
            }),
            'role': forms.TextInput(attrs={
                'id': 'role',
                'class': 'form-control role',
                'placeholder': 'user',
            }),
            'actn': forms.TextInput(attrs={
                'id': 'action',
                'class': 'form-control action',
                'placeholder': 'add an item',
            }),
            'benefit': forms.TextInput(attrs={
                'id': 'benefit',
                'class': 'form-control benefit',
                'placeholder': 'it is registered in the inventory',
            }),
        }
        labels = {
            'actn': 'Action',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(), widget=forms.HiddenInput())
