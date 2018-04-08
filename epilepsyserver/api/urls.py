
from django.conf.urls import url,include
import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers




urlpatterns = [

    url(r'^patient/$', views.PatientProfile.as_view()),
    url(r'^siezure/$', views.PatientSiezures.as_view()),


]
urlpatterns = format_suffix_patterns(urlpatterns)