from django import forms
from .models import (Artype, Code, Design, Options, Project, Requirement, Test,
                     TestApplication, UserStory)


class UserStoryForm(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = ['project', 'key', 'role', 'actn', 'benefit', 'type']
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
        self.fields['type'] = forms.CharField(widget=forms.HiddenInput())


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
            'type',
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
        self.fields['type'] = forms.CharField(widget=forms.HiddenInput())
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
            'type',
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
        self.fields['type'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['diagram'].widget.attrs.update({'class': 'form-control'})
        self.fields['document'].widget.attrs.update({'class': 'form-control'})


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = [
            'project',
            'key',
            'name',
            'document',
            'type',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(), widget=forms.HiddenInput())
        self.fields['type'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['key'].widget.attrs.update(
            {'id': 'key', 'class': 'form-control'})
        self.fields['document'].widget.attrs.update({'class': 'form-control'})


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            'project',
            'key',
            'name',
            'objective',
            'description',
            'data',
            'notes',
            'document',
            'type',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(), widget=forms.HiddenInput())
        self.fields['type'] = forms.CharField(widget=forms.HiddenInput())
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['key'].widget.attrs.update({'id': 'key'})


class TestApplicationForm(forms.ModelForm):
    class Meta:
        model = TestApplication
        fields = [
            'test',
            'application_date',
            'verdict',
            'data',
            'notes',
            'document',
        ]

    application_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test'] = forms.ModelChoiceField(
            queryset=Test.objects.all(), widget=forms.HiddenInput())
        verdict_choices = [
            ('fail', 'Fail'),
            ('pass', 'Pass'),
            ('inconclusive', 'Inconclusive'),
        ]
        self.fields['verdict'] = forms.ChoiceField(
            choices=verdict_choices, widget=forms.Select)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})


class OptionsForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = [
            'project',
            'prefix_us',
            'prefix_req',
            'prefix_design',
            'prefix_code',
            'prefix_test',
        ]
        labels = {
            'prefix_us': 'User story prefix',
            'prefix_req': 'Requirement prefix',
            'prefix_design': 'Design prefix',
            'prefix_code': 'Code prefix',
            'prefix_test': 'Test prefix',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(), widget=forms.HiddenInput())
        self.fields['prefix_us'].widget.attrs.update({'class': 'form-control'})
        self.fields['prefix_req'].widget.attrs.update({'class': 'form-control'})
        self.fields['prefix_design'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['prefix_code'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['prefix_test'].widget.attrs.update(
            {'class': 'form-control'})
