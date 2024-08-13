from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Region, District, PopulationProjection, Projection, Population, Needs, NeedsAssessment, FacilityType, PersonnelType, Sector, FurnitureType, MapPrediction, FacilityCoordinatesAndAreaName
import json
from django.views.decorators.csrf import csrf_exempt
from .population_projection_methods import calculate_projections, calculate_growth_rate, calculate_facilities_required, facility_standards, personnel_standards, calculate_personnel_required, calculate_classrooms_required, classroom_standards, calculate_dual_desks_required, dual_desk_standards, calculate_water_sources_required, water_source_standards, calculate_toilets_required, toilet_standards, calculate_skip_containers_required, skip_container_standards
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.utils.text import slugify
import urllib.parse
import random
from global_land_mask import globe
from geopy.geocoders import Nominatim
from shapely.geometry import Point, Polygon
import numpy as np
from rtree import index
import random
# import messages 
from django.contrib import messages





# Create your views here.

# home view
def home(request):
    return render(request, 'prms/home.html')


# dashboard view
@login_required(login_url='account_login')
@csrf_exempt
def dashboard(request):
    user = request.user
    population_projections = PopulationProjection.objects.filter(user=user).all()
    needs_assessments = NeedsAssessment.objects.all()
    map_predictions = MapPrediction.objects.filter(user=user).all()
    print(map_predictions)
    # filter out needs assessments that are not in the population projections
    needs = []
    for need in needs_assessments:
        if need.population_projection in population_projections:
            needs.append(need)
    

    context = {
        'population_projections':population_projections,
        # 'projections':projections,
        # 'base_years':base_years,
        # 'projection_years':projection_years
        'needs_assessments':needs,
        'map_predictions':map_predictions
    }
    
    if request.htmx:
            return render(request, 'partials/dashboard_main.html', context)
    return render(request, 'prms/dashboard.html', context)


# crud view for population projections
def crud(request):
    if request.htmx:
        mode = request.GET.get('mode', None)
        id = request.GET.get('id', None)
        print(mode)
        if mode == 'create':
            return render(request, 'forms/create_population_projection.html')
        elif mode == 'delete':
            return render(request, 'partials/delete.html', {'id': id})
        elif mode == 'report':
            return render(request, 'prms/report.html')
        elif mode == 'update':
            if id is not None:
                population_projection = PopulationProjection.objects.get(id=id)
                projections = population_projection.projections.all()
                base_year = projections.values_list('base_year', flat=True).order_by('base_year').first()
                projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year').last()
                base_population = projections.values_list('base_population', flat=True).order_by('base_population').first()
                if (population_projection.area_type == 'region'):
                    region_name = population_projection.content_object.name
                else:
                    district = District.objects.filter(name=population_projection.content_object.name).first()
                    region_name = district.region.name
        
                context = {
                    'title': population_projection.title,
                    'description': population_projection.description,
                    'growth_rate': format(population_projection.growth_rate, '.2f'),
                    'area_type': population_projection.area_type,
                    'base_year': base_year,
                    'projecting_year': projection_years,
                    'base_population': base_population,
                    'region': region_name ,
                    'district': district.name if population_projection.area_type == 'district' else None,
                    'id': population_projection.pk
                }
                return render(request, 'forms/create_population_projection.html', context)
        else:
            return render(request, 'partials/dashboard_main.html', context)
    return render(request, 'prms/dashboard.html', context)

# get regions view
def get_regions(request):
    regions = Region.objects.all()
    return JsonResponse({'regions': list(regions.values())})

def get_areas(request, area_type):
    if area_type == 'region':
        areas = Region.objects.all().order_by('name')
    elif area_type == 'district':
        areas = District.objects.all().order_by('name')
    else:
        areas = None
    context = {
        'areas': areas if areas else None
    }
    return render(request, 'partials/areas.html', context)

# get districts view
def get_districts(request):
    region = request.GET.get('region')
    districts = District.objects.filter(region__name=region)
    print(districts)
    return JsonResponse({'districts': list(districts.values())})

# calculate growth rate
def generate_unique_slug(model, base_slug):
    unique_slug = base_slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    return unique_slug

# get growth rate
def get_growth_rate(area_type, region, 
                district, 
                growth_rate_type, 
                growth_rate_manual):
    growth_rate = 0.0
    

    # Calculate growth rate if it's set to auto
    if growth_rate_type == 'auto':
        if area_type == 'region':
            region = Region.objects.get(name=region)
            pop_2010 = Population.objects.filter(object_id=region.pk)[0].population
            pop_2021 = Population.objects.filter(object_id=region.pk)[1].population
            growth_rate = calculate_growth_rate(pop_2010=pop_2010, pop_2021=pop_2021)
        elif area_type == 'district':
            district = District.objects.get(name=district)
            pop_2010 = Population.objects.filter(object_id=district.pk)[0].population
            pop_2021 = Population.objects.filter(object_id=district.pk)[1].population
            growth_rate = calculate_growth_rate(pop_2010=pop_2010, pop_2021=pop_2021)
    else:
        # Use the manual growth rate
        growth_rate = float(growth_rate_manual)
    return growth_rate
    
# create population projection view
@csrf_exempt
@login_required(login_url='account_login')
def create_or_update_population_projection(request):
    data = request.body.decode('utf-8')
    data = urllib.parse.parse_qs(data)
    data = {key: value[0] for key, value in data.items()}
    
    area_type = data.get('areaType', None)
    title = data.get('title', None)
    base_population = int(data['baseYearPopulation']) if data['baseYearPopulation'] else None
    base_year = int(data['baseYear']) if data['baseYear'] else None
    growth_rate_manual = data.get('growthRate', None)
    projecting_year = int(data['projectYear']) if data['projectYear'] else None
    description = data.get('description', None)
    growth_rate_type = data.get('growthRateType', None)
    slug = slugify(data['slug'])
    projection_id = data.get('id', None)  # To identify if it's an update
    print(data)
    # Calculate growth rate if it's set to auto
    growth_rate = get_growth_rate(
                                area_type=area_type,  growth_rate_type=growth_rate_type, 
                                growth_rate_manual=growth_rate_manual,
                                region=data.get('region', None),
                                district=data.get('district', None)
                            )
    
    
    print(f'growth_rate: {growth_rate}', type(growth_rate))
    # Calculate population projections
    projection_results = calculate_projections(base_year=base_year, projecting_year=projecting_year, base_population=base_population, growth_rate=growth_rate)

    # if the request is a POST request, create a new population projection
    if request.method == 'POST':
        slug = generate_unique_slug(PopulationProjection, slug)
        if area_type == 'region': # for region
            region = Region.objects.get(name=data['region'])
            population_projection = PopulationProjection.objects.create(
                growth_rate=growth_rate,
                description=description,
                area_type=area_type,
                title=title,
                slug=slug,
                user=request.user,
                content_object=region,
                object_id=region.pk,
                content_type=ContentType.objects.get_for_model(region)
            )
        elif area_type == 'district': # for district
            district = District.objects.get(name=data['district'])
            population_projection = PopulationProjection.objects.create(
                growth_rate=growth_rate,
                description=description,
                area_type=area_type,
                title=title,
                slug=slug,
                user=request.user,
                content_object=district,
                object_id=district.pk,
                content_type=ContentType.objects.get_for_model(district)
            )
    # if the request is a PUT request, update the population projection
    elif request.method == 'PUT': 
        print(projection_id)
        population_projection = get_object_or_404(PopulationProjection, id=projection_id)
        population_projection.title = title
        population_projection.growth_rate = growth_rate
        population_projection.description = description      
        population_projection.slug = slug
        population_projection.save()
        population_projection.projections.clear() # clear all projections before adding new ones

    # Create projections
    for result in projection_results:
        projection = Projection.objects.create(
            base_year=result['base_year'],
            base_population=result['base_population'],
            projecting_year=result['projecting_year'],
            projected_population=result['projected_population']
        )
        population_projection.projections.add(projection) # add projection to population projection

    population_projection.save()

    projections = population_projection.projections.all()

    projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
    base_years = projections.values_list('base_year', flat=True).order_by('base_year')
    base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
    projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

    custom_range = range(len(projection_years)) # create a custom range for the projections
    context = {
        'population_projection': population_projection,
        'projection_years': projection_years,
        'base_years': base_years,
        'projected_populations': projected_populations,
        'base_populations': base_populations,
        'range': custom_range,
        'growth_rate': population_projection.growth_rate
    }

    return render(request, 'prms/population_projection.html', context)

import requests

def get_geojson_from_nominatim(area_name):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': area_name,
        'format': 'json',
        'polygon_geojson': 1,
        'addressdetails': 1
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['geojson']
        else:
            return None
    else:
        response.raise_for_status()



# get population projection view
def get_population_projection(request, slug):
    population_projection = PopulationProjection.objects.get(slug=slug)
    projections = population_projection.projections.all()

    # Create a context dictionary
    projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
    base_years = projections.values_list('base_year', flat=True).order_by('base_year')
    base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
    projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

    custom_range = range(len(projection_years))

    base_year = projections.values_list('base_year', flat=True).order_by('base_year').first()
    projection_year = projections.values_list('projecting_year', flat=True).order_by('projecting_year').last()

    diff_year = projection_year - base_year

    needs_assessments = NeedsAssessment.objects.filter(population_projection=population_projection)

    # get map predictions from needs assessment
    map_predictions = MapPrediction.objects.filter(needs_assessment__in=needs_assessments).all()
    
    

    context = {
        'population_projection' :population_projection,
        'projection_years':projection_years,
        'base_years':base_years,
        'projected_populations':projected_populations,
        'base_populations':base_populations,
        'range':custom_range,
        'growth_rate': format(population_projection.growth_rate, '.2f'),
        'id': population_projection.pk,
        'diff_year':diff_year,
        'needs_assessments':needs_assessments,
        'map_predictions':map_predictions
       
    }

    # Render the child template
    child_template = get_template('prms/population_projection.html').render(context)
    

    # Check if the request is an htmx request
    if request.htmx:
        return render(request, 'prms/population_projection.html', context)
    
    # If the request is not an htmx request, render the dashboard template
    return render(request, 'prms/dashboard.html', {'child_template': child_template})


def get_population_projection_details(request, slug):
    population_projection = PopulationProjection.objects.get(slug=slug)
    projections = population_projection.projections.all()
    area_type = population_projection.area_type
    area = population_projection.content_object.name
    
    from_year = projections.values_list('base_year', flat=True).order_by('base_year').first()
    to_year = projections.values_list('projecting_year', flat=True).order_by('projecting_year').last()

    base_population = projections.values_list('base_population', flat=True).order_by('base_population').first()

    projected_population = projections.values_list('projected_population', flat=True).order_by('projected_population').last()

    # get geojson data
    # geojson = get_geojson_from_nominatim(area)
    context = {
        'population_projection':population_projection,
        # 'geojson':geojson,
        'area_type':area_type,
        'area':area,
        'from_year':from_year,
        'to_year':to_year,
        'base_population':base_population,
        'projected_population':projected_population,
        'is_education_enrollment':population_projection.is_education_enrollment
    }
    return render(request, 'partials/population_projection_details.html', context)

# get needs assessment for a population projection
def get_needs_assessment_for_population_projection(request, slug):
    sector = request.GET.get('sector', None)
    if sector is not None:
        population_projection = PopulationProjection.objects.get(slug=slug, user=request.user)
        try:
            sector = Sector.objects.get(name=sector)
            
        except Sector.DoesNotExist:
            return render(request, 'partials/health_sector.html', {'population_projection':population_projection, 'sector':sector})
        needs_assessment = NeedsAssessment.objects.filter(population_projection=population_projection).first()
        
        facility_needs = needs_assessment.needs.filter(needs_type='facility', sector=sector)
        personnel_needs = needs_assessment.needs.filter(needs_type='personnel', sector=sector)
    
        classroom_needs = needs_assessment.needs.filter(needs_type='classroom', sector=sector)
        dual_desk_needs = needs_assessment.needs.filter(needs_type='dual desk', sector=sector)

        water_needs = needs_assessment.needs.filter(needs_type='water source', sector=sector)
        print(water_needs)
        # needs for sector found
        needs_for_sector = needs_assessment.needs.filter(sector=sector)

        context = {
            'population_projection':population_projection,
            'needs_assessment':needs_assessment,
            'sector':sector ,
            'facility_needs':facility_needs ,
            'personnel_needs':personnel_needs,
            'dual_desk_needs': dual_desk_needs,
            'classroom_needs': classroom_needs,
            'needs':needs_for_sector,
            'water_needs':water_needs

        } 

    return render(request, 'partials/health_sector.html', context)

# generate report view
def generate_report(request, slug):
    population_projection = PopulationProjection.objects.get(slug=slug)
    projections = population_projection.projections.all()
    projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
    base_years = projections.values_list('base_year', flat=True).order_by('base_year')
    base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
    projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

    custom_range = range(len(projection_years))

    contex = {
        'population_projection' :population_projection,
        'projection_years':projection_years,
        'base_years':base_years,
        'projected_populations':projected_populations,
        'base_populations':base_populations,
        'range':custom_range,
        'growth_rate': population_projection.growth_rate
    }

    # Render the report template
    rendered_template = get_template('prms/report.html').render(contex)
    # convert the rendered template to pdf
    

    # Return the response
    return HttpResponse(rendered_template)


# delete population projection view
@csrf_exempt
def delete_population_projection(request, id):
    population_projection = PopulationProjection.objects.get(id=id)
    population_projection.delete()
    user = request.user
    population_projections = PopulationProjection.objects.filter(user=user).all()
    needs_assessments = NeedsAssessment.objects.all()
    # filter out needs assessments that are not in the population projections
    needs = []
    for need in needs_assessments:
        if need.population_projection in population_projections:
            needs.append(need)
    

    context = {
        'population_projections':population_projections,
        # 'projections':projections,
        # 'base_years':base_years,
        # 'projection_years':projection_years
        'needs_assessments':needs
    }

    return render(request, 'partials/dashboard_main.html', context)


# get population projection form
def get_population_projection_form(request):
    template = get_template('forms/create_population_projection.html').render()
    return JsonResponse({'form_template':template})


# create needs assessment view
def create_needs_assesment(request):
    population_projections = PopulationProjection.objects.all()
    required_facilities = []
    required_personnels = []
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = urllib.parse.parse_qs(data)
        data = {key: value[0] for key, value in data.items()}
        sector = data.get('sector', None)
        projection_slug = data.get('projectedPopulation', None)
        need_type = data.get('type', None)
        facility_numbers = data.get('facilityNumbers', None)
        personnel_numbers = data.get('personnelNumbers', None)
        facility_numbers = json.loads(facility_numbers) if facility_numbers else None
        personnel_numbers = json.loads(personnel_numbers) if personnel_numbers else None
        needs_assessment_slug = ''
       

        population_projection = PopulationProjection.objects.filter(slug=projection_slug, user=request.user, is_education_enrollment=False).first()

        projections = population_projection.projections.all()
        projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
        base_years = projections.values_list('base_year', flat=True).order_by('base_year')
        base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
        projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

        populations = []
        for i in range(len(projection_years)):
            populations.append(
                {
                    'year':base_years[i],
                    'population':base_populations[i]
                }
            )
        populations.append(
            {
                'year':projection_years.last(),
                'population':projected_populations.last()
            }
        )


        
        # check if sector is health
        if sector == 'health':
            if need_type == 'facility':
                # check if there is an existing needs_assessment for this particular projection
                needs_assessment = NeedsAssessment.objects.filter(population_projection=population_projection).first()
                
                try:
                    sector = Sector.objects.get(name=sector)
                except Sector.DoesNotExist:
                    sector = Sector.objects.create(name=sector, description='Health sector', slug=slugify(sector))

                # check if there is an existing needs_assessment
                if needs_assessment:
                    # calculate the number of personnel required for each year and population
                    for population in populations:
                        print(population['year'], population['population'])
                        results = calculate_facilities_required(
                            population=population['population'],
                            facility_numbers=facility_numbers,
                            year = population['year'],
                            standards=facility_standards
                        )
                        required_facilities.append(results)
                    
                    formatted_results = []
                    for i in required_facilities:
                        for j in i:
                            formatted_results.append(j)

                    facility_needs = needs_assessment.needs.filter(needs_type='facility')
                    
                    # check if there are existing needs
                    if facility_needs:
                        # delete and create new ones
                        facility_needs.delete()
                        for i in formatted_results:
                            facility = FacilityType.objects.create(
                                year = i['year'],
                                type_name = i['facility_type'],
                                required = i['required'],
                                standard = i['standard'],
                                new_need = i['new_need'],
                                suplus = i['suplus'],
                                available = i['available'],
                                population = i['population']
                            )
                            need = Needs.objects.create(
                                needs_type = 'facility',
                                object_id = facility.pk,
                                content_type = ContentType.objects.get_for_model(facility),
                                content_object = facility,
                                sector = sector
                            )
                            needs_assessment.needs.add(need)
                        needs_assessment.save()

                    # create new needs
                    else:
                        #save into database
                        for i in required_facilities:
                            for j in i:
                                facility = FacilityType.objects.create(
                                    year = j['year'],
                                    type_name = j['facility_type'],
                                    required = j['required'],
                                    standard = j['standard'],
                                    new_need = j['new_need'],
                                    suplus = j['suplus'],
                                    available = j['available'],
                                    population = j['population']
                                )
                                need = Needs.objects.create(
                                    needs_type = 'facility',
                                    object_id = facility.pk,
                                    content_type = ContentType.objects.get_for_model(facility),
                                    content_object = facility,
                                    sector = sector
                                )
                                needs_assessment.needs.add(need)
                        needs_assessment.save()
                        needs_assessment_slug = needs_assessment.slug
                # create a new needs assessment
                else:
                    # create a new needs assessment
                    slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
                    slug = generate_unique_slug(NeedsAssessment, slug)

                    # check if sector exists
                    try:
                        sector = Sector.objects.get(name=sector)
                    except Sector.DoesNotExist:
                        sector = Sector.objects.create(name=sector, description='Health sector', slug=slugify(sector))
                    
                    # create a new needs assessment
                    needs_assessment = NeedsAssessment.objects.create(
                        population_projection = population_projection,
                        slug = slug
                    )

                    # calculate the number of personnel required for each year and population
                    for population in populations:
                        print(population['year'], population['population'])
                        results = calculate_facilities_required(
                            population=population['population'],
                            facility_numbers=facility_numbers,
                            year = population['year'],
                            standards=facility_standards
                        )
                        required_facilities.append(results)
                    print(required_facilities)

                    #save into database
                    for i in required_facilities:
                        for j in i:
                            facility = FacilityType.objects.create(
                                year = j['year'],
                                type_name = j['facility_type'],
                                required = j['required'],
                                standard = j['standard'],
                                new_need = j['new_need'],
                                suplus = j['suplus'],
                                available = j['available'],
                                population = j['population']
                            )
                            # create a new need
                            need = Needs.objects.create(
                                needs_type = 'facility',
                                object_id = facility.pk,
                                content_type = ContentType.objects.get_for_model(facility),
                                content_object = facility,
                                sector = sector
                            )
                            print(need)
                            needs_assessment.needs.add(need)
                          
                    needs_assessment.save()
                    needs_assessment_slug = needs_assessment.slug
                
            # check if need type is personnel
            elif need_type == 'personnel':
                # check if there is an existing needs_assessment for this particular projection
                needs_assessment = NeedsAssessment.objects.get(population_projection=population_projection)
                
                try:
                    sector = Sector.objects.get(name=sector)
                except Sector.DoesNotExist:
                    sector = Sector.objects.create(name=sector, description='Health sector', slug=slugify(sector))

                # check if there is an existing needs_assessment
                if needs_assessment:
                    # calculate the number of personnel required for each year and population
                    for population in populations:
                        print(population['year'], population['population'])
                        results = calculate_personnel_required(
                            population=population['population'],
                            personnel_numbers=personnel_numbers,
                            year = population['year'],
                            standards=personnel_standards
                        )
                        required_personnels.append(results)
                    
                    formatted_results = []
                    for i in required_personnels:
                        for j in i:
                            formatted_results.append(j)
                    
                    # 
                    personnel_needs = needs_assessment.needs.filter(needs_type='personnel')
                    if personnel_needs:
                        # delete and create new one
                        need.delete()
                        for i in formatted_results:
                            personnel = PersonnelType.objects.create(
                                year = i['year'],
                                type_name = i['personnel_type'],
                                required = i['required'],
                                standard = i['standard'],
                                new_need = i['new_need'],
                                suplus = i['suplus'],
                                available = i['available'],
                                population = i['population']
                            )
                            need = Needs.objects.create(
                                needs_type = 'personnel',
                                object_id = personnel.pk,
                                content_type = ContentType.objects.get_for_model(personnel),
                                content_object = personnel,
                                sector = sector
                            )
                            needs_assessment.needs.add(need)
                        needs_assessment.save()
                            
                    else:
                        #save into database
                        for i in required_personnels:
                            for j in i:
                                personnel = PersonnelType.objects.create(
                                    year = j['year'],
                                    type_name = j['personnel_type'],
                                    required = j['required'],
                                    standard = j['standard'],
                                    new_need = j['new_need'],
                                    suplus = j['suplus'],
                                    available = j['available'],
                                    population = j['population']
                                )
                                need = Needs.objects.create(
                                    needs_type = 'personnel',
                                    object_id = personnel.pk,
                                    content_type = ContentType.objects.get_for_model(personnel),
                                    content_object = personnel,
                                    sector = sector
                                )
                                needs_assessment.needs.add(need)
                        needs_assessment.save()
                        needs_assessment_slug = needs_assessment.slug
                else:
                    # create a new needs assessment
                    slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
                    slug = generate_unique_slug(NeedsAssessment, slug)

                    try:
                        sector = Sector.objects.get(name=sector)
                    except Sector.DoesNotExist:
                        sector = Sector.objects.create(name=sector, description='Health sector', slug=slugify(sector))

                    needs_assessment = NeedsAssessment.objects.create(
                        population_projection = population_projection,
                        slug = slug
                    )
                    # calculate the number of personnel required for each year and population
                    for population in populations:
                        print(population['year'], population['population'])
                        results = calculate_personnel_required(
                            population=population['population'],
                            personnel_numbers=personnel_numbers,
                            year = population['year'],
                            standards=personnel_standards
                        )
                        required_personnels.append(results)

                    #save into database
                    for i in required_personnels:
                        for j in i:
                            personnel = PersonnelType.objects.create(
                                year = j['year'],
                                type_name = j['personnel_type'],
                                required = j['required'],
                                standard = j['standard'],
                                new_need = j['new_need'],
                                suplus = j['suplus'],
                                available = j['available'],
                                population = j['population']
                            )
                            need = Needs.objects.create(
                                needs_type = 'personnel',
                                object_id = personnel.pk,
                                content_type = ContentType.objects.get_for_model(personnel),
                                content_object = personnel,
                                sector = sector

                            )
                            needs_assessment.needs.add(need)

                    needs_assessment.save()
                    needs_assessment_slug = needs_assessment.slug
        
        else:
            pass
        
        context = get_needs_assessment_context(slug=needs_assessment_slug, request=request)
        
        child_template = get_template('prms/get_needs_assessment.html').render(context)

        
            
        return render(request, 'prms/get_needs_assessment.html', context)
        
    return render(request, 'prms/dashboard.html', {'child_template': child_template}) 


@csrf_exempt
def education_needs_assessment(request):

    if request.method == 'POST':
        # get data from htmx ajax
        data = request.body.decode('utf-8')
        data = urllib.parse.parse_qs(data)
        data = {key: value[0] for key, value in data.items()}
        print(data)
        
        sector = data.get('sector', None)
        education_type = data.get('type', None)
        base_year = data.get('baseYear', None)
        projection_year = data.get('projectionYear', None)
        growth_rate = data.get('growthRate', None)
        base_population = data.get('basePopulation', None)
        classroom_numbers = data.get('schoolNumbers', None)
        dual_desk_numbers = data.get('dualDeskNumbers', None)
        area = data.get('area', None)
        area_type = data.get('areaType', None)
        population_projection_slug = data.get('populationProjection', None)

        classroom_numbers = json.loads(classroom_numbers) if classroom_numbers else None
        dual_desk_numbers = json.loads(dual_desk_numbers) if dual_desk_numbers else None

        required_classrooms= []
        required_dual_desks = []
        try:
            population_projection = PopulationProjection.objects.filter(slug=population_projection_slug, user=request.user, is_education_enrollment=True).first()
        except PopulationProjection.DoesNotExist:
            population_projection = None

        if not population_projection:
            # calculate population projections
            projection_results = calculate_projections(base_year=int(base_year), projecting_year=int(projection_year), base_population=int(base_population), growth_rate=float(growth_rate))

            # create a new population projection
            slug = slugify(f'{sector}-{education_type}')
            slug = generate_unique_slug(PopulationProjection, slug)

            if area_type == 'region':
                region = Region.objects.get(name=area)
                population_projection = PopulationProjection.objects.create(
                    growth_rate=growth_rate,
                    description = f'Population Projection for {sector} enrolment in {area} {area_type}',
                    area_type=area_type,
                    title=f'Population Projection for {sector} enrolment in {area}',
                    slug=slug,
                    user=request.user,
                    content_object=region,
                    object_id=region.pk,
                    content_type=ContentType.objects.get_for_model(region)
                )
            elif area_type == 'district':
                district = District.objects.get(name=area)
                population_projection = PopulationProjection.objects.create(
                    growth_rate=growth_rate,
                    description=f'Population Projection for {sector} enrolment in {area} {area_type}',
                    area_type=area_type,
                    title=f'Population Projection for {sector} enrolment in {area}',
                    slug=slug,
                    user=request.user,
                    content_object=district,
                    object_id=district.pk,
                    content_type=ContentType.objects.get_for_model(district)
                )

            # Create projections
            for result in projection_results:
                projection = Projection.objects.create(
                    base_year=result['base_year'],
                    base_population=result['base_population'],
                    projecting_year=result['projecting_year'],
                    projected_population=result['projected_population']
                )
                population_projection.projections.add(projection) # add projection to population projection
            population_projection.save()

        projections = population_projection.projections.all()
        projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
        base_years = projections.values_list('base_year', flat=True).order_by('base_year')
        base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
        projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

        custom_range = range(len(projection_years)) # create a custom range for the projections

        base_year = projections.values_list('base_year', flat=True).order_by('base_year').first()
        projection_year = projections.values_list('projecting_year', flat=True).order_by('projecting_year').last()

        diff_year = projection_year - base_year

        context = {
            'population_projection' :population_projection,
            'projection_years':projection_years,
            'base_years':base_years,
            'projected_populations':projected_populations,
            'base_populations':base_populations,
            'range':custom_range,
            'growth_rate': population_projection.growth_rate,
            'id': population_projection.pk,
            'diff_year':diff_year
        }

        

        # needs assessment for education
        needs_assessment_slug = ''
        if education_type == 'classroom':
            # check if there is an existing needs_assessment for this particular projection
            needs_assessment = NeedsAssessment.objects.filter(population_projection=population_projection).first()
            try:
                sector = Sector.objects.get(name=sector)
            except Sector.DoesNotExist:
                sector = Sector.objects.create(name=sector, description='Education sector', slug=slugify(sector))

            if needs_assessment:
                # calculate the number of personnel required for each year and population
                for population in projections:
                    results = calculate_classrooms_required(
                        population=population.base_population,
                        classroom_numbers=classroom_numbers,
                        year = population.base_year,
                        standards=classroom_standards
                    )
                    required_classrooms.append(results)
                
                formatted_results = []
                for i in required_classrooms:
                    for j in i:
                        formatted_results.append(j)
                
                #save into database
                needs = needs_assessment.needs.all().filter(needs_type='classroom')

                if needs:
                   # delete and create new one
                    needs.delete()
                    for i in formatted_results:
                        classroom = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['classroom_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'classroom',
                            object_id = classroom.pk,
                            content_type = ContentType.objects.get_for_model(classroom),
                            content_object = classroom,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                    needs_assessment.save()
                       
                else:
                    #save into database
                    for i in required_classrooms:
                        for j in i:
                            classroom = FacilityType.objects.create(
                                year = j['year'],
                                type_name = j['classroom_type'],
                                required = j['required'],
                                standard = j['standard'],
                                new_need = j['new_need'],
                                suplus = j['suplus'],
                                available = j['available'],
                                population = j['population']
                            )
                            need = Needs.objects.create(
                                needs_type = 'classroom',
                                object_id = classroom.pk,
                                content_type = ContentType.objects.get_for_model(classroom),
                                content_object = classroom,
                                sector = sector
                            )
                            needs_assessment.needs.add(need)
                    needs_assessment.save()
                    needs_assessment_slug = needs_assessment.slug

            else:
                # create a new needs assessment
                slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
                slug = generate_unique_slug(NeedsAssessment, slug)

                try:
                    sector = Sector.objects.get(name=sector)
                except Sector.DoesNotExist:
                    sector = Sector.objects.create(name=sector, description='Education sector', slug=slugify(sector))

                needs_assessment = NeedsAssessment.objects.create(
                    population_projection = population_projection,
                    slug = slug
                )
                # calculate the number of personnel required for each year and population
                for population in projections:
                    results = calculate_classrooms_required(
                        population=population.base_population,
                        classroom_numbers=classroom_numbers,
                        year = population.base_year,
                        standards=classroom_standards
                    )
                    required_classrooms.append(results)

                #save into database
                for i in required_classrooms:
                    for j in i:
                        classroom = FacilityType.objects.create(
                            year = j['year'],
                            type_name = j['classroom_type'],
                            required = j['required'],
                            standard = j['standard'],
                            new_need = j['new_need'],
                            suplus = j['suplus'],
                            available = j['available'],
                            population = j['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'classroom',
                            object_id = classroom.pk,
                            content_type = ContentType.objects.get_for_model(classroom),
                            content_object = classroom,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                needs_assessment.save()
                needs_assessment_slug = needs_assessment.slug

        elif education_type == 'dual_desk':
            # check if there is an existing needs_assessment for this particular projection
            needs_assessment = NeedsAssessment.objects.filter(population_projection=population_projection).first()
            try:
                sector = Sector.objects.get(name=sector)
            except Sector.DoesNotExist:
                sector = Sector.objects.create(name=sector, description='Education sector', slug=slugify(sector))

            if needs_assessment:
                # calculate the number of personnel required for each year and population
                for population in projections:
                    results = calculate_dual_desks_required(
                        population=population.base_population,
                        dual_desk_numbers=dual_desk_numbers,
                        year = population.base_year,
                        standards=dual_desk_standards
                    )
                    required_dual_desks.append(results)
                
                formatted_results = []
                for i in required_dual_desks:
                    for j in i:
                        formatted_results.append(j)

        
                
                #save into database
                needs = needs_assessment.needs.all().filter(needs_type='dual desk')
                if needs:
                    # delete and create new one
                    needs.delete()
                    for i in formatted_results:
                        dual_desk = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['dual_desk_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'dual desk',
                            object_id = dual_desk.pk,
                            content_type = ContentType.objects.get_for_model(dual_desk),
                            content_object = dual_desk,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                    needs_assessment.save()
                else:
                        #save into database 
                        for i in required_dual_desks:
                            for j in i:
                                dual_desk = FurnitureType.objects.create(
                                    year = j['year'],
                                    type_name = j['dual_desk_type'],
                                    required = j['required'],
                                    standard = j['standard'],
                                    new_need = j['new_need'],
                                    suplus = j['suplus'],
                                    available = j['available'],
                                    population = j['population']
                                )
                                need = Needs.objects.create(
                                    needs_type = 'dual desk',
                                    object_id = dual_desk.pk,
                                    content_type = ContentType.objects.get_for_model(dual_desk),
                                    content_object = dual_desk,
                                    sector = sector
                                )
                                needs_assessment.needs.add(need)
                        needs_assessment.save()
                        needs_assessment_slug = needs_assessment.slug
            else:
                # create a new needs assessment
                slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
                slug = generate_unique_slug(NeedsAssessment, slug)

                try:
                    sector = Sector.objects.get(name=sector)
                except Sector.DoesNotExist:
                    sector = Sector.objects.create(name=sector, description='Education sector', slug=slugify(sector))

                needs_assessment = NeedsAssessment.objects.create(
                    population_projection = population_projection,
                    slug = slug
                )
                # calculate the number of personnel required for each year and population
                for population in projections:
                    results = calculate_dual_desks_required(
                        population=population.base_population,
                        dual_desk_numbers=dual_desk_numbers,
                        year = population.base_year,
                        standards=dual_desk_standards
                    )
                    required_dual_desks.append(results)

                #save into database
                for i in required_dual_desks:
                    for j in i:
                        dual_desk = FurnitureType.objects.create(
                            year = j['year'],
                            type_name = j['dual_desk_type'],
                            required = j['required'],
                            standard = j['standard'],
                            new_need = j['new_need'],
                            suplus = j['suplus'],
                            available = j['available'],
                            population = j['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'dual desk',
                            object_id = dual_desk.pk,
                            content_type = ContentType.objects.get_for_model(dual_desk),
                            content_object = dual_desk,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                needs_assessment.save()
                needs_assessment_slug = needs_assessment.slug
        
        need_context = get_needs_assessment_context(request=request, slug=needs_assessment.slug)
        

        # append context to needs_context
        if population_projection_slug:
            return render (request, 'prms/get_needs_assessment.html', need_context)
        else:
            return render(request, 'prms/population_projection.html', context)

@csrf_exempt
def utility_needs_assessment(request):
    data = request.body.decode('utf-8')
    data = urllib.parse.parse_qs(data)
    data = {key: value[0] for key, value in data.items()}
    sector = data.get('sector', None)
    utility_type = data.get('type', None)
    population_projection_slug = data.get('populationProjection', None)
    water_source_numbers = data.get('waterSourceNumbers', None)
    water_source_numbers = json.loads(water_source_numbers) if water_source_numbers else None
    toilet_numbers = data.get('toiletNumbers', None)
    toilet_numbers = json.loads(toilet_numbers) if toilet_numbers else None
    skip_container_numbers = data.get('skipContainerNumbers', None)
    skip_container_numbers = json.loads(skip_container_numbers) if skip_container_numbers else None

    required_water_sources = []
    required_toilets = []
    required_skip_containers = []

    try:
        population_projection = PopulationProjection.objects.filter(slug=population_projection_slug, user=request.user, is_education_enrollment=False).first()
    except PopulationProjection.DoesNotExist:
        population_projection = None

    if population_projection:
        projections = population_projection.projections.all()
        projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
        base_years = projections.values_list('base_year', flat=True).order_by('base_year')
        base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
        projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

        populations = []
        for i in range(len(projection_years)):
            populations.append(
                {
                    'year':base_years[i],
                    'population':base_populations[i]
                }
            )
        populations.append(
            {
                'year':projection_years.last(),
                'population':projected_populations.last()
            }
        )

        # check if there is an existing needs_assessment for this particular projection
        
        try:
            sector = Sector.objects.get(name=sector)
            needs_assessment = NeedsAssessment.objects.get(population_projection=population_projection)
        except Sector.DoesNotExist:
            sector = Sector.objects.create(name=sector, description='Utility sector', slug=slugify(sector))
        except NeedsAssessment.DoesNotExist:
            needs_assessment = None

        if needs_assessment:
            # calculate the number of personnel required for each year and population
            if utility_type == 'water':
                for population in projections:
                    results = calculate_water_sources_required(
                        population=population.base_population,
                        water_source_numbers=water_source_numbers,
                        year = population.base_year,
                        standards=water_source_standards
                    )
                    required_water_sources.append(results)

                formatted_results = []
                for i in required_water_sources:
                    for j in i:
                        formatted_results.append(j)

                needs = needs_assessment.needs.all()
                water_needs = needs.filter(needs_type='water source')
                if water_needs:
                    # delete all existing water needs and create new ones
                    water_needs.delete()
                    for i in formatted_results:
                        water_source = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['water_source_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'water source',
                            object_id = water_source.pk,
                            content_type = ContentType.objects.get_for_model(water_source),
                            content_object = water_source,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                    needs_assessment.save()

  
                else:
                    for i in formatted_results:
                        water_source = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['water_source_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'water source',
                            object_id = water_source.pk,
                            content_type = ContentType.objects.get_for_model(water_source),
                            content_object = water_source,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                needs_assessment.save()

            elif utility_type == 'toilet':
                for population in projections:
                    results = calculate_toilets_required(
                        population=population.base_population,
                        toilet_numbers=toilet_numbers,
                        year = population.base_year,
                        standards=toilet_standards
                    )
                    required_toilets.append(results)
                
                formatted_results = []
                for i in required_toilets:
                    for j in i:
                        formatted_results.append(j)
                needs = needs_assessment.needs.all()
                toilet_needs = needs.filter(needs_type='toilet')
                if toilet_needs:
                    # delete an create new ones
                    toilet_needs.delete()
                    for i in formatted_results:
                        toilet = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['toilet_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'toilet',
                            object_id = toilet.pk,
                            content_type = ContentType.objects.get_for_model(toilet),
                            content_object = toilet,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                    needs_assessment.save()

                    
                else:
                    for i in formatted_results:
                        toilet = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['toilet_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'toilet',
                            object_id = toilet.pk,
                            content_type = ContentType.objects.get_for_model(toilet),
                            content_object = toilet,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                needs_assessment.save()
               
            
            elif utility_type == 'wasteDisposal':
                for population in projections:
                    results = calculate_skip_containers_required(
                        population=population.base_population,
                        skip_container_numbers=skip_container_numbers,
                        year = population.base_year,
                        standards=skip_container_standards
                    )
                    required_skip_containers.append(results)

                formatted_results = []
                for i in required_skip_containers:
                    for j in i:
                        formatted_results.append(j)

                needs = needs_assessment.needs.all()
                skip_container_needs = needs.filter(needs_type='skip container')
                if skip_container_needs:
                    # delete and create new ones
                    skip_container_needs.delete()
                    for i in formatted_results:
                        skip_container = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['skip_container_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'skip container',
                            object_id = skip_container.pk,
                            content_type = ContentType.objects.get_for_model(skip_container),
                            content_object = skip_container,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                    needs_assessment.save
                    
                else:
                    for i in formatted_results:
                        skip_container = FacilityType.objects.create(
                            year = i['year'],
                            type_name = i['skip_container_type'],
                            required = i['required'],
                            standard = i['standard'],
                            new_need = i['new_need'],
                            suplus = i['suplus'],
                            available = i['available'],
                            population = i['population']
                        )
                        need = Needs.objects.create(
                            needs_type = 'skip container',
                            object_id = skip_container.pk,
                            content_type = ContentType.objects.get_for_model(skip_container),
                            content_object = skip_container,
                            sector = sector
                        )
                        needs_assessment.needs.add(need)
                
        else:
            # create a new needs assessment
            slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
            slug = generate_unique_slug(NeedsAssessment, slug)

            try:
                sector = Sector.objects.get(name=sector)
            except Sector.DoesNotExist:
                sector = Sector.objects.create(name=sector, description='Utility sector', slug=slugify(sector))

            needs_assessment = NeedsAssessment.objects.create(
                population_projection = population_projection,
                slug = slug
            )
            
            if utility_type == 'water':
                for population in projections:
                    results = calculate_water_sources_required(
                        population=population.base_population,
                        water_source_numbers=water_source_numbers,
                        year = population.base_year,
                        standards=water_source_standards
                    )
                    required_water_sources.append(results)

                formatted_results = []
                for i in required_water_sources:
                    for j in i:
                        formatted_results.append(j)
                for i in formatted_results:
                    water_source = FacilityType.objects.create(
                        year = i['year'],
                        type_name = i['water_source_type'],
                        required = i['required'],
                        standard = i['standard'],
                        new_need = i['new_need'],
                        suplus = i['suplus'],
                        available = i['available'],
                        population = i['population']
                    )
                    need = Needs.objects.create(
                        needs_type = 'water source',
                        object_id = water_source.pk,
                        content_type = ContentType.objects.get_for_model(water_source),
                        content_object = water_source,
                        sector = sector
                    )
                    needs_assessment.needs.add(need)
                needs_assessment.save()
                
            elif utility_type == 'toilet':
                for population in projections:
                    results = calculate_toilets_required(
                        population=population.base_population,
                        toilet_numbers=toilet_numbers,
                        year = population.base_year,
                        standards=toilet_standards
                    )
                    required_toilets.append(results)
                
                formatted_results = []
                for i in required_toilets:
                    for j in i:
                        formatted_results.append(j)
                for i in formatted_results:
                    toilet = FacilityType.objects.create(
                        year = i['year'],
                        type_name = i['toilet_type'],
                        required = i['required'],
                        standard = i['standard'],
                        new_need = i['new_need'],
                        suplus = i['suplus'],
                        available = i['available'],
                        population = i['population']
                    )
                    need = Needs.objects.create(
                        needs_type = 'toilet',
                        object_id = toilet.pk,
                        content_type = ContentType.objects.get_for_model(toilet),
                        content_object = toilet,
                        sector = sector
                    )
                    needs_assessment.needs.add(need)
                needs_assessment.save()
          

            elif utility_type == 'wasteDisposal':
                for population in projections:
                    results = calculate_skip_containers_required(
                        population=population.base_population,
                        skip_container_numbers=skip_container_numbers,
                        year = population.base_year,
                        standards=skip_container_standards
                    )
                    required_skip_containers.append(results)

                formatted_results = []
                for i in required_skip_containers:
                    for j in i:
                        formatted_results.append(j)
                for i in formatted_results:
                    skip_container = FacilityType.objects.create(
                        year = i['year'],
                        type_name = i['skip_container_type'],
                        required = i['required'],
                        standard = i['standard'],
                        new_need = i['new_need'],
                        suplus = i['suplus'],
                        available = i['available'],
                        population = i['population']
                    )
                    need = Needs.objects.create(
                        needs_type = 'skip container',
                        object_id = skip_container.pk,
                        content_type = ContentType.objects.get_for_model(skip_container),
                        content_object = skip_container,
                        sector = sector
                    )
                    needs_assessment.needs.add(need)
                needs_assessment.save()
         

        context = get_needs_assessment_context(slug=needs_assessment.slug, request=request)
        context['utility_type'] = utility_type
        

    return render(request, 'prms/get_needs_assessment.html', context)
 
# get needs assessment context
def get_needs_assessment_context(request, slug):
    population_projections = PopulationProjection.objects.filter(user=request.user).all()
    needs_assessment = NeedsAssessment.objects.get(slug=slug)
    health_needs = needs_assessment.needs.filter(sector__name='health')
    education_needs = needs_assessment.needs.filter(sector__name='education')
    
    # get distinct facility types
    facility_types_with_available = []
    personnels_types_with_available = []
    for need in health_needs:
        if need.needs_type == 'facility':
            facility = need.content_object
            facility_types_with_available.append(
                {
                    'facility':facility.type_name,
                    'available':facility.available
                }
            )
        elif need.needs_type == 'personnel':
            personnel = need.content_object
            personnels_types_with_available.append(
                {
                    'personnel_type':personnel.type_name,
                    'available':personnel.available
                }
            )

    
    unique_facilities = []
    for i in facility_types_with_available:
        if i not in unique_facilities:
            unique_facilities.append(i)
    facility_types_with_available = unique_facilities

    unique_personnels = []
    for i in personnels_types_with_available:
        if i not in unique_personnels:
            unique_personnels.append(i)
    personnels_types_with_available = unique_personnels

    personnel_needs = health_needs.filter(needs_type='personnel',)
    facility_needs = health_needs.filter(needs_type='facility')

    classroom_needs = education_needs.filter(needs_type='classroom')
    dual_desk_needs = education_needs.filter(needs_type='dual desk')
    water_needs = needs_assessment.needs.filter(needs_type='water source')
    skip_container_needs = needs_assessment.needs.filter(needs_type='skip container')

    context = {
        'population_projections':population_projections,
        'facility_types_with_available':facility_types_with_available,
        'personnels_types_with_available':personnels_types_with_available,
        'personnel_needs':personnel_needs,
        'facility_needs':facility_needs,
        'classroom_needs':classroom_needs,
        'dual_desk_needs':dual_desk_needs,
        'slug':slug,
        'needs_assessment':needs_assessment,
        'water_needs':water_needs,
        'skip_container_needs': skip_container_needs
    }
    return context


# get needs assessment view
def get_needs_assessment(request, slug):
    population_projections = PopulationProjection.objects.all()
    needs_assessment = NeedsAssessment.objects.get(slug=slug)
    
    
    
    # get distinct facility types
    context = get_needs_assessment_context(slug=slug, request=request)
   

    child_template = get_template('prms/get_needs_assessment.html').render(context)

    if request.htmx:
        return render(request, 'prms/get_needs_assessment.html', context)
    
    return render(request, 'prms/dashboard.html', {'child_template': child_template})

# update needs assessment view
def update_needs_assessment(request, slug):
    population_projections = PopulationProjection.objects.all()
    required_facilities = []
    required_personnels = []
    needs_assessment = NeedsAssessment.objects.get(slug=slug)
    data = json.loads(request.body)
    if request.method == 'PUT':
        sector = data.get('sector', None)
        projection_slug = data.get('projectedPopulation', None)
        facility_numbers = data.get('facilityNumbers', None)
        personnel_numbers = data.get('personnelNumbers', None)
        need_type = data.get('needType', None)

        # update needs assessment
    
        population_projection = PopulationProjection.objects.get(slug=projection_slug)
        needs_assessment.population_projection = population_projection

        # update slug if the sector or population projection has changed
        new_slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
        if new_slug != needs_assessment.slug:
            needs_assessment.slug = generate_unique_slug(NeedsAssessment, new_slug)
        

        # calculate the number of facilities required for each year and population
        projections = population_projection.projections.all()
        projection_years = projections.values_list('projecting_year', flat=True).order_by('projecting_year')
        base_years = projections.values_list('base_year', flat=True).order_by('base_year')
        base_populations = projections.values_list('base_population', flat=True).order_by('base_population')
        projected_populations = projections.values_list('projected_population', flat=True).order_by('projected_population')

        populations = []
        for i in range(len(projection_years)):
            populations.append(
                {
                    'year':base_years[i],
                    'population':base_populations[i]
                }
            )
        populations.append(
            {
                'year':projection_years.last(),
                'population':projected_populations.last()
            }
        )

        # get all needs
        if sector == 'health':
            try:
                sector = Sector.objects.get(name=sector)
            except Sector.DoesNotExist:
                sector = Sector.objects.create(name=sector, description='Health sector', slug=slugify(sector))
                
            needs = needs_assessment.needs.filter(sector__name=sector)
            if need_type == 'personnel':
                needs = needs.filter(needs_type='personnel')
                for population in populations:
                    print(population['year'], population['population'])
                    results = calculate_personnel_required(
                        population=population['population'],
                        personnel_numbers=personnel_numbers,
                        year = population['year'],
                        standards=personnel_standards
                    )
                    required_personnels.append(results)
                
                formatted_personnels = []
                for i in required_personnels:
                    for j in i:
                        formatted_personnels.append(j)
                # update needs 
                for (index, need) in enumerate(needs):
                    personnel = need.content_object
                    personnel.available = formatted_personnels[index]['available']
                    personnel.required = formatted_personnels[index]['required']
                    personnel.standard = formatted_personnels[index]['standard']
                    personnel.new_need = formatted_personnels[index]['new_need']
                    personnel.suplus = formatted_personnels[index]['suplus']
                    personnel.population = formatted_personnels[index]['population']
                    personnel.save()
                
            else:
                needs = needs.filter(needs_type='facility')
                for population in populations:
                    print(population['year'], population['population'])
                    results = calculate_facilities_required(
                        population=population['population'],
                        facility_numbers=facility_numbers,
                        year = population['year'],
                        standards=facility_standards
                    )
                    required_facilities.append(results)
                
                
                formatted_facilities = []
                for i in required_facilities:
                    for j in i:
                        formatted_facilities.append(j)
            
                # update needs
                for (index, need) in enumerate(needs):
                    facility = need.content_object
                    facility.available = formatted_facilities[index]['available']
                    facility.required = formatted_facilities[index]['required']
                    facility.standard = formatted_facilities[index]['standard']
                    facility.new_need = formatted_facilities[index]['new_need']
                    facility.suplus = formatted_facilities[index]['suplus']
                    facility.population = formatted_facilities[index]['population']
                    facility.save()
       
        context = get_needs_assessment_context(slug=new_slug, request=request)
        needs_assessment_template = get_template('prms/get_needs_assessment.html').render(context)
        return JsonResponse({'template': needs_assessment_template, 'slug':slug})
    
    child_template = get_template('prms/needs_assessment.html').render({'population_projections':population_projections})

    return render(request, 'prms/dashboard.html', {'child_template': child_template}) 


def udpate_needs_assessment_page(request, slug):
    needs_type = request.GET.get('needs_type', None)
    sector = request.GET.get('sector', None)
    population_projections = PopulationProjection.objects.filter(user=request.user).all()
    needs_assessment = NeedsAssessment.objects.get(slug=slug)
    sector = get_object_or_404(Sector, name=sector)
    context = get_needs_assessment_context(slug=slug, request=request)

    if needs_type == 'personnel':
        personnel_needs = needs_assessment.needs.filter(needs_type='personnel', sector=sector)
        context['personnel_needs'] = personnel_needs
        context['needs_type'] = 'personnel'
        context['sector'] = 'health'
        
    elif needs_type == 'facility':
        facility_needs = needs_assessment.needs.filter(needs_type='facility', sector=sector)
        context['facility_needs'] = facility_needs
        context['needs_type'] = 'facility'
        context['sector'] = 'health'

    


    child_template = get_template('prms/needs_assessment.html').render(context)
    # if ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'template':child_template,})

    if request.htmx:
        return render(request, 'prms/needs_assessment.html', context)
    return render(request, 'prms/dashboard.html', {'child_template': child_template})

@csrf_exempt
def delete_needs(request, slug, needs_type, **kwargs):
    try:
        needs_assessment = get_object_or_404(NeedsAssessment, slug=slug)
        needs_to_delete = needs_assessment.needs.filter(needs_type=needs_type)
        needs_to_delete.delete()
        context = get_needs_assessment_context(slug=slug, request=request)
        needs_assessment_template = get_template('prms/get_needs_assessment.html').render(context)

        # check if need assessment has any needs
        if not needs_assessment.needs.all():
            needs_assessment.delete()
            user = request.user
            population_projections = PopulationProjection.objects.filter(user=user).all()
            needs_assessments = NeedsAssessment.objects.all()
            # filter out needs assessments that are not in the population projections
            needs = []
            for need in needs_assessments:
                if need.population_projection in population_projections:
                    needs.append(need)

            context = {
                'population_projections':population_projections,
                'needs_assessments':needs
            }
            
            return render(request, 'partials/dashboard_main.html', context)
        return render(request, 'prms/get_needs_assessment.html', context)
    except (NeedsAssessment.DoesNotExist, ValueError):
        return HttpResponse(status=404)


# delete needs assessment view
@csrf_exempt
def delete_needs_assessment(request, slug):
    user = request.user
    population_projections = PopulationProjection.objects.filter(user=user).all()
    if request.method == 'DELETE':
        needs_assessment = NeedsAssessment.objects.get(slug=slug)
        needs_assessment.delete()
        

        needs_assessments = NeedsAssessment.objects.all()
        # filter out needs assessments that are not in the population projections
        needs = []
        for need in needs_assessments:
            if need.population_projection in population_projections:
                needs.append(need)

    context = {
        'population_projections':population_projections,
        'needs_assessments':NeedsAssessment.objects.all()
    }
    return render(request, 'partials/dashboard_main.html', context)
 


# needs assessment view
@csrf_exempt
def needs_assessment(request, slug=None):
    all_population_projections = PopulationProjection.objects.filter(user=request.user).all()
    
    population_projections = all_population_projections.filter(is_education_enrollment=False)

    education_enrollment_projections = all_population_projections.filter(is_education_enrollment=True)

 

    #
    if request.method == 'POST' and slug is None:
        return create_needs_assesment(request)
    elif slug is not None:
        if request.method == 'GET':
            return get_needs_assessment(request, slug)
        elif request.method == 'PUT':
            return update_needs_assessment(request, slug)
        elif request.method == 'DELETE':
            return delete_needs_assessment(request, slug)

    context = {
        'population_projections':population_projections,
        'education_enrollment_projections':education_enrollment_projections
    }

    child_template = get_template('prms/needs_assessment.html').render(context)
    if request.htmx:
        return render(request, 'prms/needs_assessment.html', context)
    return render(request, 'prms/dashboard.html', {'child_template': child_template})    



# map prediction
@csrf_exempt
def map_prediction(request):
    needs_assessments = NeedsAssessment.objects.all()
    
    context = {
        'needs_assessments':needs_assessments
    }
    if request.htmx:
        return render(request, 'prms/map_prediction.html', context)

    if request.method == 'POST':
        img = request.FILES.get('image')
        facility_coordinates = request.POST.get('facility_coordinates')
        pk = request.POST.get('needs_assessment')
        map_prediction_pk = request.POST.get('map_prediction', None)
        if map_prediction_pk:
            map_prediction = MapPrediction.objects.get(pk=map_prediction_pk)
            # delete existing image
            map_prediction.image.delete()
            map_prediction.image = img

            # save facility coordinates
            facility_coordinates = json.loads(facility_coordinates)
            facility_coordinates_and_area_name = map_prediction.facility_coordinates_and_area_name.all()

            for i in facility_coordinates_and_area_name:
                for j in facility_coordinates:
                    if i.facility_name == j['facility']:
                        i.lattitude = j['lat']
                        i.longitude = j['lon']
                        i.area_name = j['areaName']
                        i.save()
                        

            map_prediction.save()
            map_prediction_template = get_template('prms/get_map_prediction.html').render({'map_prediction':map_prediction})
            return JsonResponse({'message':'success', 'template':map_prediction_template, 'status':'success'})

        
        else:
            map_prediction_slug = generate_unique_slug(MapPrediction, f'map-prediction-{pk}')
            # save map prediction
            needs_assessment = get_object_or_404(NeedsAssessment, pk=pk)
            map_prediction = MapPrediction.objects.create(
                needs_assessment = needs_assessment,
                image = img,
                user = request.user,
                slug=map_prediction_slug
            )

            # save facility coordinates
            facility_coordinates = json.loads(facility_coordinates)
            print(img, facility_coordinates, pk)
            for i in facility_coordinates:
                facility = FacilityCoordinatesAndAreaName.objects.create(
                    facility_name = i['facility'],
                    lattitude = i['lat'],
                    longitude = i['lon'],
                    area_name = i['areaName'],
                )

                map_prediction.facility_coordinates_and_area_name.add(facility)
            map_prediction.save()
            map_prediction_template = get_template('prms/get_map_prediction.html').render({'map_prediction':map_prediction})

            url = '/map-prediction/'+map_prediction.slug+'/'

            return JsonResponse({'message':'success', 'template':map_prediction_template, 'url':url, 'status':'success'})
    else:
        child_template = get_template('prms/map_prediction.html').render(context)
        return render(request, 'prms/dashboard.html', {'child_template': child_template})
        


    
    

def get_map_prediction(request, slug):
    map_prediction = MapPrediction.objects.get(slug=slug)
    needs_assessment = map_prediction.needs_assessment
    population_projection = needs_assessment.population_projection
    base_year = population_projection.projections.first().base_year
    projecting_year = population_projection.projections.last().projecting_year
    

    facility_coordinates = map_prediction.facility_coordinates_and_area_name.all()
    facility_needs = needs_assessment.needs.filter(needs_type='facility', sector__name='health')
    
    context = {
        'map_prediction':map_prediction,
        'facility_coordinates':facility_coordinates,
        'needs_assessment':needs_assessment,
        'population_projection':population_projection,
        'facility_needs':facility_needs,
        'base_year':base_year,
        'projecting_year':projecting_year,
    }

    if request.method == 'DELETE':
        map_prediction.delete()
        user = request.user
        population_projections = PopulationProjection.objects.filter(user=user).all()
        needs_assessments = NeedsAssessment.objects.all()
        map_predictions = MapPrediction.objects.filter(user=user).all()
        # filter out needs assessments that are not in the population projections
        needs = []
        for need in needs_assessments:
            if need.population_projection in population_projections:
                needs.append(need)
        

        context = {
            'population_projections':population_projections,
            'needs_assessments':needs,
            'map_predictions':map_predictions
        }
        dashboard_template = get_template('prms/dashboard.html').render(context)
        url = '/dashboard/'
        return JsonResponse({'message':'success', 'status':'success', 'template':dashboard_template, 'url':url})

    child_template = get_template('prms/get_map_prediction.html').render(context)
    if request.htmx:
        return render(request, 'prms/get_map_prediction.html', context)
    return render(request, 'prms/dashboard.html', {'child_template': child_template})

def get_needs_assessment_detail(request, pk):
    needs_assessment = NeedsAssessment.objects.get(id=pk)
    print(needs_assessment)
    population_projection = needs_assessment.population_projection
    print(population_projection)
    area_name = str(population_projection.content_object.name).lower()
    area_type = population_projection.area_type
    # get coordinates bounds of area_name using geopy
    geo_url = f'https://nominatim.openstreetmap.org/search?format=json&q={area_name} region'
    context = {}
    required_facilities = []
    facility_coordinates = []
    bounds = ""
    APP_ID = "llUkylLlqtIChTjVZtP3"
    API_KEY = "QolF50IlVf_RPFJtNCUd0F-c0nhtHOLSirkhNjlUa4c"
    here_geo_url = f'https://geocode.search.hereapi.com/v1/geocode?q={area_name}&in=countryCode:GHA&apiKey={API_KEY}'
    geolocator = Nominatim(user_agent="PNSM")
    base_year = population_projection.projections.first().base_year
    projecting_year = population_projection.projections.last().projecting_year
    # get health facility needs 
    facility_needs = needs_assessment.needs.filter(needs_type='facility', sector__name='health')

    if facility_needs:
        try:
            temp_response = requests.get(url=here_geo_url)
        except requests.HTTPError as e :
            messages.error(request, f'Network error, {e}')
        except requests.ConnectionError as e:
            messages.error(request, f'Connection error, {e}')
        if temp_response.status_code == 200:
            temp_response = temp_response.json()
            if temp_response.get('items'):
                temp_response = temp_response.get('items')[0]
                lat = temp_response.get('position').get('lat')
                lon = temp_response.get('position').get('lng')
                area_name = geolocator.reverse(f'{lat}, {lon}').address
                print(f'AREA_NAME: {area_name}')

                context['area_coordinates'] = [lat, lon]
                bounds = temp_response.get('mapView')
                print(bounds)
        else:
            messages.error(request,' An error occured')

        # get facilities_needs for the projecting year
        for need in facility_needs:
            if need.content_object.year == projecting_year:
                facility = need.content_object
                required_facilities.append(
                    {
                        'facility':facility.type_name,
                        'required':facility.required,
                    }
                )
        # Desired minimum distance from the boundary (in degrees)
        min_distance = 0.1

        # Calculate the adjusted bounding box
        min_lat = bounds['south'] + min_distance
        max_lat = bounds['north'] - min_distance
        min_lon = bounds['west'] + min_distance
        max_lon = bounds['east'] - min_distance    

        # Generate random coordinates within the adjusted bounding box
        for i in required_facilities:
            if i['required'] > 0:
                while True:
                    lat = random.uniform(min_lat, max_lat)
                    lon = random.uniform(min_lon, max_lon)
                    is_land = globe.is_land(lat, lon)
                    if is_land:
                        try:
                            area_name = geolocator.reverse(f'{lat}, {lon}').address
                        except Exception as e:
                            messages.error(request, f'Error {e}')
                        
                        facility_coordinates.append(
                            {
                                'facility':i['facility'],
                                'lat':lat,
                                'lon':lon,
                                'required':i['required'],
                                'area_name':area_name
                            }
                        )
                        break

    context['facility_coordinates'] = facility_coordinates
    context['area_name'] = population_projection.content_object.name
    context['base_year'] = base_year
    context['projecting_year'] = projecting_year
    context['area_type'] = area_type
    context['needs_types'] = needs_assessment.needs.all().values_list('needs_type', flat=True).distinct()
    context['base_population'] = population_projection.projections.first().base_population
    context['projected_population'] = population_projection.projections.last().projected_population
    
    needs_assessment_template = get_template('partials/needs_assessment_details.html').render(context)

    facility_needs_template = get_template('partials/facility_needs_template.html').render({'facility_needs':facility_needs})

    
        
    return JsonResponse({
        'needs_assessment_template':needs_assessment_template,
        'facility_needs_template':facility_needs_template,
        'facility_coordinates':facility_coordinates,
        'area_coordinates':context['area_coordinates'] if 'area_coordinates' in context else None
    })

