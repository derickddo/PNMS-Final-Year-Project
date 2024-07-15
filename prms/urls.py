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
    path('needs-assessment/', views.needs_assessment, name='create_need_assessment'),
    path('needs-assessment/<str:slug>', views.needs_assessment, name='manage_need_assessment'),
    path('needs-assessment/<str:slug>/edit', views.udpate_needs_assessment_page, name='update_needs_assessment_page'),
    path('needs-assessment/<str:slug>/need/<str:needs_type>/delete', views.delete_needs, name='delete_needs'),
    path('get-needs-assement-for-population-projection/<str:slug>', views.get_needs_assessment_for_population_projection, name='get_needs_assessment_for_population_projection'),
    path('get-population-projection-details/<str:slug>', views.get_population_projection_details, name='population_projection_details'),
]
   