from django.contrib import admin

from questionnaire_app import models

admin.site.register(models.Admin)
admin.site.register(models.Employee)
admin.site.register(models.Department)
admin.site.register(models.Question)
admin.site.register(models.Questionnaire)
admin.site.register(models.Answer)
admin.site.register(models.Choice)