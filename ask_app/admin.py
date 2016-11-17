from django.contrib import admin
from ask_app import models

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
class ProfileAdmin(admin.ModelAdmin):
    pass
    #list_display = ('title',)


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Profile, ProfileAdmin)



# Register your models here.
