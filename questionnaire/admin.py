from django.contrib import admin
from .models import Question



class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'user', 'email', 'year', 'wake_up', 'go_to_bed', 'how_clean', 'guests', 'more_introverted_or_extroverted', 'ideal_rent', 'pfp']}),
    ]
    list_display = ('email', 'year')


admin.site.register(Question, QuestionAdmin)


