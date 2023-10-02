from django import forms
from .models import Design, Project, Requirement, UserStory


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
            'document',
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
                'id': 'description',
                'class': 'form-control',
                'placeholder': 'Briefly explain what is the purpose of this '
                               'use case',
            }),
            'preconditions': forms.TextInput(attrs={
                'id': 'preconditions',
                'class': 'form-control',
                'placeholder': 'The initial state before the use case is '
                               'executed',
            }),
            'sequence': forms.TextInput(attrs={
                'id': 'seq',
                'class': 'form-control',
                'placeholder': 'The sequence of steps',
            }),
            'postcondition': forms.TextInput(attrs={
                'id': 'postcondition',
                'class': 'form-control',
                'placeholder': 'The resulting state after the execution of '
                               'the steps',
            }),
            'notes': forms.TextInput(attrs={
                'id': 'notes',
                'class': 'form-control',
                'placeholder': 'Any other comments about this use case',
            }),
            'document': forms.TextInput(attrs={
                'id': 'document',
                'class': 'form-control',
                'placeholder': 'Link to an external file (e.g. '
                               'https://docs.google.com/...)',
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


class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = [
            'project',
            'key',
            'name',
            'diagram',
            'document',
        ]
        widgets = {
            'key': forms.TextInput(attrs={
                'id': 'key',
                'class': 'form-control',
                'type': 'number',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(), widget=forms.HiddenInput())
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['diagram'].widget.attrs.update({'class': 'form-control'})
        self.fields['document'].widget.attrs.update({'class': 'form-control'})
