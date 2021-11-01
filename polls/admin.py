"""Manage admin page on web app."""

from django.contrib import admin

from .models import Choice, Question, Vote


class ChoiceInline(admin.StackedInline):
    """Define How many choice for each polls."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Define detail of each polls in admin page."""

    list_filter = ['pub_date']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information',
         {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
