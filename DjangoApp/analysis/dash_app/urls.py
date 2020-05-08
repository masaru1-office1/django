from django.urls import path,include
from . import views
from . import dash_apps

app_name='dash_app'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('population_passenger/',views.populaton_passenger_view,name='population_passenger'),
]
    
