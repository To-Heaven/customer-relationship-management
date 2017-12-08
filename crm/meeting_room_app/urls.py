from django.conf.urls import url, include
from django.contrib import admin

from meeting_room_app import views

urlpatterns = [
    url(r'list_orders/$', views.list_orders),
    url(r'manage_orders^/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', views.list_orders),
]