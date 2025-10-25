from django import template

register = template.Library()

@register.filter
def active_questions_count(survey):
    """Return count of active questions for a survey"""
    return survey.questions.filter(is_active=True).count()
