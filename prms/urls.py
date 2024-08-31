from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('regions/', views.get_regions, name='regions'),
    path('districts/', views.get_districts, name='districts'),
    path('towns/', views.get_towns, name='towns'),
    path('create-population-projection/', views.create_or_update_population_projection, name='create_population_projection'),
    path('population-projection/<str:slug>/', views.get_population_projection, name='population_projection'),
    path('generate-report/<str:slug>/', views.generate_report, name='generate_report'),
    path('crud/', views.crud, name='crud'),

    path('delete-projection/<int:id>/', views.delete_population_projection, name='delete_population_projection'),
    path('needs-assessment/', views.needs_assessment, name='needs_assessment'),
    path('create-needs-assessment/', views.create_needs_assesment, name='create_need_assessment'),
    path('get-needs-assessment/<str:slug>/',views.get_needs_assessment, name='get_needs_assessment'),
    path('delete-needs-assessment/<str:slug>/', views.delete_needs_assessment, name='delete_needs_assessment'),
    path('needs-assessment/<str:slug>', views.needs_assessment, name='manage_need_assessment'),
    path('needs-assessment/<str:slug>/edit', views.udpate_needs_assessment_page, name='update_needs_assessment_page'),
    path('needs-assessment/<str:slug>/need/<str:needs_type>/delete', views.delete_needs, name='delete_needs'),
    path('get-needs-assement-for-population-projection/<str:slug>', views.get_needs_assessment_for_population_projection, name='get_needs_assessment_for_population_projection'),
    path('get-population-projection-details/<str:pk>', views.get_population_projection_details, name='population_projection_details'),
    path('education-needs-assessment/', views.education_needs_assessment, name='education_needs_assessment'),
    path('get-areas/<str:area_type>', views.get_areas, name='get_areas'),
    path('delete-needs-assessment/<str:slug>/', views.delete_needs_assessment, name='delete_needs_assessment'),
    path('utility-needs-assessment/', views.utility_needs_assessment, name='utility_needs_assessment'),
    path('map-prediction/', views.map_prediction, name='map_prediction'),
    path('map-prediction/<str:slug>/', views.get_map_prediction, name='get_map_prediction'),
    path('get-needs-assessment-details/<int:pk>/', views.get_needs_assessment_detail, name='needs_assessment_details'),
    path('search/', views.search, name='search'),
]
   