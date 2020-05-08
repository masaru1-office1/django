from django.urls import path
from . import views

app_name='index_app'

urlpatterns = [
    path('',views.index_page,name='index'),
]
    