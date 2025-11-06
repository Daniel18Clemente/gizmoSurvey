from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Survey, Question, Section


class UserRegistrationForm(UserCreationForm):
    """Extended user registration form for student accounts only"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    section = forms.ModelChoiceField(queryset=Section.objects.filter(is_active=True), required=True, empty_label="Select Section")
    student_id = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='student',  # Automatically set to student
                section=self.cleaned_data['section'],
                student_id=self.cleaned_data['student_id']
            )
        return user


class SurveyForm(forms.ModelForm):
    """Form for creating and editing surveys"""
    class Meta:
        model = Survey
        fields = ['title', 'description', 'sections', 'due_date', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sections': forms.CheckboxSelectMultiple(),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make due_date required
        self.fields['due_date'].required = True
        # Only show active sections
        self.fields['sections'].queryset = Section.objects.filter(is_active=True)


class QuestionForm(forms.ModelForm):
    """Form for creating and editing questions"""
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'is_required', 'options', 'likert_min', 'likert_max', 'likert_labels']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'likert_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'likert_max': forms.NumberInput(attrs={'class': 'form-control'}),
            # Keep these hidden; UI handles inputs dynamically
            'options': forms.HiddenInput(),
            'likert_labels': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
        
        # Replace JSON-backed fields with simple text fields to avoid JSON validation
        if 'options' in self.fields:
            self.fields['options'] = forms.CharField(required=False, widget=forms.HiddenInput())
        if 'likert_labels' in self.fields:
            self.fields['likert_labels'] = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_options(self):
        """Convert textarea input to list for multiple choice options"""
        options_text = self.cleaned_data.get('options', '')
        if isinstance(options_text, str):
            options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
            return options
        return options_text

    def clean_likert_labels(self):
        """Convert textarea input to list for likert labels"""
        labels_text = self.cleaned_data.get('likert_labels', '')
        if isinstance(labels_text, str):
            labels = [label.strip() for label in labels_text.split('\n') if label.strip()]
            return labels
        return labels_text


class QuestionBulkForm(forms.Form):
    """Form for bulk operations on questions"""
    ACTION_CHOICES = [
        ('delete', 'Delete Selected'),
        ('reorder', 'Reorder Selected'),
        ('toggle_required', 'Toggle Required Status'),
        ('change_type', 'Change Question Type'),
    ]
    
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    question_ids = forms.CharField(widget=forms.HiddenInput())
    new_order = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new order numbers separated by commas'}))
    new_type = forms.ChoiceField(choices=Question.QUESTION_TYPES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))


class SurveySettingsForm(forms.ModelForm):
    """Enhanced form for survey settings management"""
    class Meta:
        model = Survey
        fields = ['title', 'description', 'sections', 'due_date', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sections': forms.CheckboxSelectMultiple(),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make due_date required
        self.fields['due_date'].required = True
        # Only show active sections
        self.fields['sections'].queryset = Section.objects.filter(is_active=True)
        # Add CSS classes to all form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})


class AssignmentForm(forms.Form):
    """Form for managing survey assignments"""
    sections = forms.ModelMultipleChoiceField(
        queryset=Section.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=True
    )
    is_active = forms.BooleanField(
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})


class SectionBulkForm(forms.Form):
    """Form for bulk operations on sections"""
    ACTION_CHOICES = [
        ('activate', 'Activate Selected'),
        ('deactivate', 'Deactivate Selected'),
    ]
    
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    section_ids = forms.CharField(widget=forms.HiddenInput())


class SurveyResponseForm(forms.Form):
    """Dynamic form for survey responses"""
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        
        for question in survey.questions.filter(is_active=True):
            field_name = f'question_{question.id}'
            
            if question.question_type == 'multiple_choice':
                # Ensure options is a list and not None/empty
                options = question.options if isinstance(question.options, list) and question.options else []
                choices = [(opt, opt) for opt in options]
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=question.is_required,
                    label=question.question_text
                )
            
            elif question.question_type == 'likert_scale':
                choices = [(i, i) for i in range(question.likert_min, question.likert_max + 1)]
                # Ensure likert_labels is a list and not None/empty before using
                if question.likert_labels and isinstance(question.likert_labels, list) and len(question.likert_labels) > 0:
                    choices = [(i, question.likert_labels[i-question.likert_min] if (i-question.likert_min) < len(question.likert_labels) else str(i)) 
                              for i in range(question.likert_min, question.likert_max + 1)]
                
                # Coerce to int so cleaned_data is an integer
                self.fields[field_name] = forms.TypedChoiceField(
                    choices=choices,
                    coerce=int,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=question.is_required,
                    label=question.question_text
                )
            
            elif question.question_type == 'short_answer':
                self.fields[field_name] = forms.CharField(
                    max_length=500,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    required=question.is_required,
                    label=question.question_text
                )
            
            elif question.question_type == 'long_answer':
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                    required=question.is_required,
                    label=question.question_text
                )


class SectionForm(forms.ModelForm):
    """Form for creating and editing sections"""
    class Meta:
        model = Section
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
