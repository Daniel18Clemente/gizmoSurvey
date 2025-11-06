from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Section, Survey, Question, SurveyResponse, Answer


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'due_date', 'created_at']
    list_filter = ['is_active', 'created_at', 'due_date']
    search_fields = ['title', 'description']
    filter_horizontal = ['sections']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'survey', 'question_type', 'is_required', 'order']
    list_filter = ['question_type', 'is_required']
    search_fields = ['question_text']
    ordering = ['survey', 'order']


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['student', 'survey', 'submitted_at', 'is_complete']
    list_filter = ['is_complete', 'submitted_at']
    search_fields = ['student__first_name', 'student__last_name', 'survey__title']
    readonly_fields = ['submitted_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['response', 'question', 'answer_text', 'answer_number', 'answer_choice']
    list_filter = ['question__question_type']
    search_fields = ['answer_text', 'answer_choice']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
