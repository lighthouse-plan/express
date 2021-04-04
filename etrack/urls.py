from django.urls import path

from . import views

app_name = 'etrack'
urlpatterns = [
    path('<str:shop>/', views.index, name='index'),
    path('<str:shop>/search/', views.search, name='search'),
]