from django.contrib import admin

from meeting_room_app import models


admin.site.register(models.User)
admin.site.register(models.Order)
admin.site.register(models.MeetingRoom)