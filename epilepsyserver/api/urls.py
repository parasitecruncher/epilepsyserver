
from django.conf.urls import url,include
import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers




urlpatterns = [

    url(r'^patient/(?P<pk>[a-zA-Z0-9_]+)/$', views.PatientProfile.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)