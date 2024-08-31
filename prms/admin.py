from django.contrib import admin
from .models import Region, District, Population, PopulationProjection, Projection, User, NeedsAssessment, Needs, FacilityType, PersonnelType, Sector, FurnitureType, MapPrediction, FacilityCoordinatesAndAreaName, Town
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Q
from django.contrib import messages

# Register your models here
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'map_url')
    search_fields = ('name',)

class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PopulationAdmin(admin.ModelAdmin):
    list_display = ['population', 'year', 'content_object']
    search_fields = ['year', 'population']
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # Custom search logic for content_object
        try:
            content_object_ids = list(Region.objects.filter(name__icontains=search_term).values_list('id', flat=True))
            content_object_ids += list(District.objects.filter(name__icontains=search_term).values_list('id', flat=True))
            # content_object_ids += list(Town.objects.filter(name__icontains=search_term).values_list('id', flat=True))
            
            if content_object_ids:
                queryset |= self.model.objects.filter(
                    Q(object_id__in=content_object_ids) &
                    (Q(content_type__model='region') | Q(content_type__model='district') | Q(content_type__model='town'))
                )
        except Exception as e:
            # Handle any exceptions that may occur
            self.message_user(request, f"Error occurred during search: {e}", level=messages.ERROR)

        return queryset, use_distinct
    
    

admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(PopulationProjection)
admin.site.register(Projection)
admin.site.register(User)
admin.site.register(NeedsAssessment)
admin.site.register(Needs)
admin.site.register(FacilityType)
admin.site.register(PersonnelType)
admin.site.register(Sector)
admin.site.register(FurnitureType)
admin.site.register(MapPrediction)
admin.site.register(FacilityCoordinatesAndAreaName)
admin.site.register(Town)
    


