from django.conf.urls import url

from questionnaire_app import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^add_questionnaire/$', views.add_questionnaire),
    url(r'^list_questionnaire/$', views.list_questionnaire),
    url(r'^manage_questionnaire/(?P<questionnaire_id>\d+)/$', views.manage_questionnaire, name='manage_questionnaire'),
    url(r'^show_score/(?P<department_id>\d+)/(?P<questionnaire_id>\d+)/$', views.show_score, name='show_score'),
    url(r'^get_questionnaire_page/(?P<department_id>\d+)/(?P<questionnaire_id>\d+)/$', views.get_questionnaire_page)
]
