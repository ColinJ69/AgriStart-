from django.contrib import admin
from django.urls import path, include
import main.views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls') ),
    path('tutorials', v.tutorials, name='tutorials')
]