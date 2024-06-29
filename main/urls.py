from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('score', views.score, name='score'),
    path('tutorials', views.tutorials, name='tutorials'),
    path('tutorials/growing', views.growing, name='growing'),
    path('tutorials/sustainable', views.sustainable, name='sustainable'),
    path('recommendations', views.recommendation, name='recommendation'),
    path('detection', views.detection, name='detection'),
    path('grants', views.grants, name='grants')
    ]