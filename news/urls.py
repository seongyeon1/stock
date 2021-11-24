from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsList.as_view(), name='index'),
]