from django.contrib import admin
from main.models import *

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name','domain', 'university', 'address', 'location',)
    list_filter = ['domain', 'university', 'location']
        
        
class AttemptedQuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('question', 'player', 'time', 'marks_obtained', 'time_taken', 'server_time_taken', 'answered',)
    list_display = ('time',  'question', 'player', 'marks_obtained', 'time_taken', 'server_time_taken', 'answered',)
    list_filter = ['time', 'player']
    search_fields = ['player', 'question_title']
    date_hierarchy = 'time'

admin.site.register(Professor, ProfessorAdmin)
admin.site.register(ConfrenceProfile)
admin.site.register(Confrence)
#admin.site.register(AttemptedQuestion, AttemptedQuestionAdmin)
