from django.urls import path

from . import views

app_name = 'etrack'
urlpatterns = [
    # path('kawaguchi/', views.index_kawa, name='index_kawa'),
    # path('kawaguchi/ensure/', views.ensure_kawa, name='ensure_kawa'),
    path('ikebukuro/', views.index_ike, name='index_ike'),
    path('ikebukuro/search/', views.search_ike, name='search_ike'),
]