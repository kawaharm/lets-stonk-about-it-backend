from django.urls import path
from . import views

# Set app name for templates
app_name = 'tweets'

# Paths
urlpatterns = [
    path('', views.index, name='index')
]
