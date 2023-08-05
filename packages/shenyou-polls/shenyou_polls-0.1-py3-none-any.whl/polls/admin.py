from django.contrib import admin
from .models import Question,Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('标题',{'fields':['question_text']}),
        ('日期',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    list_filter = ['pub_date']
    search_fields=['question_text']
    list_display = ('question_text','pub_date','was_published_recently')
    inlines = [ChoiceInline]
    

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)