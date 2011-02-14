from django.contrib import admin
from multilingual.admin import MultilingualModelAdmin
from models import Question, Topic
from datetime import datetime
            

class TopicAdmin(MultilingualModelAdmin):
    pass
    # prepopulated_fields = {'slug':('name',)} # django-admin chokes on this

    
class QuestionAdmin(MultilingualModelAdmin):
  
    list_display = ['text', 'sort_order', 'created_by', 'created_on', 'updated_by', 'updated_on', 'status']

    def save_model(self, request, obj, form, change): 
        '''
        Overrided because I want to also set who created this instance.
        '''
        instance = form.save( commit=False )
        if instance.id is None:
            new = True
            instance.created_by = request.user
                
        instance.updated_by = request.user
        instance.save()
        
        return instance

admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
