from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('regions/', views.get_regions, name='regions'),
    path('districts/', views.get_districts, name='districts'),
    path('create-population-projection/', views.create_or_update_population_projection, name='create_population_projection'),
    path('population-projection/<str:slug>/', views.get_population_projection, name='population_projection'),
    path('generate-report/<str:slug>/', views.generate_report, name='generate_report'),
    path('crud/', views.crud, name='crud'),

    path('delete-projection/<int:id>/', views.delete_population_projection, name='delete_population_projection'),
    path('needs-assessment/', views.needs_assessment, name='needs_assessment'),
]
   