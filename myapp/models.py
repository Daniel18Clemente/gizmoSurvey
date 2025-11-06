from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Section(models.Model):
    """Represents a class/section that surveys can be assigned to"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, help_text="Whether this section is active (not soft deleted)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class UserProfile(models.Model):
    """Extended user profile with role and section information"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Whether this user profile is active (not soft deleted)")
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class Survey(models.Model):
    """Main survey model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_surveys')
    sections = models.ManyToManyField(Section, related_name='surveys')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1, help_text="Incremented when survey is edited")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_open(self):
        """Check if survey is currently open for submissions"""
        if not self.is_active:
            return False
        if self.due_date and timezone.now() > self.due_date:
            return False
        return True


class Question(models.Model):
    """Survey questions with different types"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('likert_scale', 'Likert Scale'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, help_text="Whether this question is active (not soft deleted)")
    order = models.PositiveIntegerField(default=0)
    
    # For multiple choice questions
    options = models.JSONField(default=list, blank=True)
    
    # For Likert scale questions
    likert_min = models.IntegerField(default=1)
    likert_max = models.IntegerField(default=5)
    likert_labels = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.survey.title} - {self.question_text[:50]}..."


class SurveyResponse(models.Model):
    """Individual survey responses"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_responses')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=True)
    survey_version = models.PositiveIntegerField(default=1, help_text="Version of survey when response was submitted")
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.survey.title}"


class Answer(models.Model):
    """Individual answers to questions"""
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    answer_number = models.IntegerField(null=True, blank=True)
    answer_choice = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['response', 'question']
    
    def __str__(self):
        return f"{self.response.student.get_full_name()} - {self.question.question_text[:30]}..."
