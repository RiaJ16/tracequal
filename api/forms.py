from django import forms
from .models import Project, Requirement, UserStory


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


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = [
            'project',
            'key',
            'name',
            'description',
            'preconditions',
            'sequence',
            'alt_sequence',
            'postcondition',
            'notes',
            # 'document',
        ]
        widgets = {
            'key': forms.TextInput(attrs={
                'id': 'key',
                'class': 'form-control',
                'type': 'number',
            }),
            'name': forms.TextInput(attrs={
                'id': 'name',
                'class': 'form-control',
                'placeholder': 'Name of the use case',
            }),
            'description': forms.TextInput(attrs={
                'id': 'action',
                'class': 'form-control',
                'placeholder': '',
            }),
            'preconditions': forms.TextInput(attrs={
                'id': 'benefit',
                'class': 'form-control',
                'placeholder': '',
            }),
            'sequence': forms.TextInput(attrs={
                'id': 'benefit',
                'class': 'form-control',
                'placeholder': '',
            }),
            'postcondition': forms.TextInput(attrs={
                'id': 'benefit',
                'class': 'form-control',
                'placeholder': '',
            }),
            'notes': forms.TextInput(attrs={
                'id': 'benefit',
                'class': 'form-control',
                'placeholder': '',
            }),
        }
        labels = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(), widget=forms.HiddenInput())
        self.fields['alt_sequence'] = forms.JSONField(
            widget=forms.HiddenInput(), required=False)
