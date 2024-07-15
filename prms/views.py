from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Region, District, PopulationProjection, Projection, Population, Needs, NeedsAssessment, FacilityType, PersonnelType
import json
from django.views.decorators.csrf import csrf_exempt
from .population_projection_methods import calculate_projections, calculate_growth_rate, calculate_facilities_required, facility_standards, personnel_standards, calculate_personnel_required
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.utils.text import slugify




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
    data = json.loads(request.body)
    area_type = data.get('areaType', None)
    title = data.get('title', None)
    base_population = int(data['baseYearPopulation'])
    base_year = int(data['baseYear'])
    growth_rate_manual = data.get('growthRate', None)
    projecting_year = int(data['projectYear'])
    description = data.get('description', None)
    growth_rate_type = data['growthRateType']
    slug = slugify(data['slug'])
    projection_id = data.get('id', None)  # To identify if it's an update
    
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
    rendered_template = get_template('prms/population_projection.html').render({
        'population_projection': population_projection,
        'projection_years': projection_years,
        'base_years': base_years,
        'projected_populations': projected_populations,
        'base_populations': base_populations,
        'range': custom_range,
        'growth_rate': population_projection.growth_rate
    })

    return JsonResponse({'message': 'Population projection processed successfully', 'rendered_template': rendered_template, 'slug':population_projection.slug})
   

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
        'projected_population':projected_population
    }
    return render(request, 'partials/population_projection_details.html', context)

# get needs assessment for a population projection
def get_needs_assessment_for_population_projection(request, slug):
    sector = request.GET.get('sector', None)
    if sector is not None:
        population_projection = PopulationProjection.objects.get(slug=slug)
        
        needs_assessments = NeedsAssessment.objects.filter(population_projection=population_projection, sector=sector)
        facility_needs = []
        personnel_needs = []
        for need_assessment in needs_assessments:
            needs = need_assessment.needs.all()
            for need in needs:
                if need.needs_type == 'facility':
                    facility_needs.append(need)
                elif need.needs_type == 'personnel':
                    personnel_needs.append(need)
            
        context = {
            'population_projection':population_projection,
            'needs_assessments':needs_assessments,
            'facility_needs':facility_needs,
            'personnel_needs':personnel_needs,
            'sector':sector,
            'needs_assessment_slug':needs_assessments.first().slug if needs_assessments else None
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
    

    context = {
        'population_projections':population_projections,
        # 'projections':projections,
        # 'base_years':base_years,
        # 'projection_years':projection_years
    }

    return render(request, 'partials/dashboard_main.html', context)

# get delete template
def get_delete_template(request):
    template = get_template('partials/delete.html').render()
    
    if request.htmx:
        return render(request, 'partials/delete.html')
    return JsonResponse({'html':template})

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
        data = json.loads(request.body)
        sector = data.get('sector', None)
        projection_slug = data.get('projectedPopulation', None)
        need_type = data.get('type', None)
        facility_numbers = data.get('facilityNumbers', None)
        personnel_numbers = data.get('personnelNumbers', None)
        needs_assessment_slug = ''
       

        population_projection = PopulationProjection.objects.get(slug=projection_slug)

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
        
        

        if need_type == 'facility':
            # check if there is an existing needs_assessment for this particular projection
            needs_assessment = NeedsAssessment.objects.filter(population_projection=population_projection).first()
            print(needs_assessment)
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
                            content_object = facility
                        )
                        needs_assessment.needs.add(need)
                needs_assessment.save()
                needs_assessment_slug = needs_assessment.slug

            else:
                # create a new needs assessment
                slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
                slug = generate_unique_slug(NeedsAssessment, slug)

                needs_assessment = NeedsAssessment.objects.create(
                    sector=sector,
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
                            content_object = facility
                        )
                        needs_assessment.needs.add(need)

                needs_assessment.save()
                needs_assessment_slug = needs_assessment.slug
            

        elif need_type == 'personnel':
            # check if there is an existing needs_assessment for this particular projection
            needs_assessment = NeedsAssessment.objects.get(population_projection=population_projection)
            print(needs_assessment)
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
                            content_object = personnel
                        )
                        needs_assessment.needs.add(need)
                needs_assessment.save()
                needs_assessment_slug = needs_assessment.slug
            else:
                # create a new needs assessment
                slug = slugify(f'{sector}-{population_projection.area_type}-{population_projection.content_object.name}')
                slug = generate_unique_slug(NeedsAssessment, slug)

                needs_assessment = NeedsAssessment.objects.create(
                    sector=sector,
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
                            content_object = personnel
                        )
                        needs_assessment.needs.add(need)

                needs_assessment.save()
                needs_assessment_slug = needs_assessment.slug
            

                

        elif need_type == 'equipment':
            pass
        elif need_type == 'furniture':
            pass
        else:
            pass
        
        context = get_needs_assessment_context(slug=needs_assessment_slug, request=request)
        
        needs_assessment_template = get_template('prms/get_needs_assessment.html').render(context) 
            
        return JsonResponse({'template': needs_assessment_template, 'slug':needs_assessment_slug})
    
    child_template = get_template('prms/get_needs_assessment.html').render(context)

    return render(request, 'prms/dashboard.html', {'child_template': child_template}) 

# get needs assessment context
def get_needs_assessment_context(request, slug):
    population_projections = PopulationProjection.objects.filter(user=request.user).all()
    needs_assessment = NeedsAssessment.objects.get(slug=slug)
    needs = needs_assessment.needs.all()
    
    # get distinct facility types
    facility_types_with_available = []
    personnels_types_with_available = []
    for need in needs:
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

    personnel_needs = needs.filter(needs_type='personnel')
    facility_needs = needs.filter(needs_type='facility')
    context = {
        'population_projections':population_projections,
        'facility_types_with_available':facility_types_with_available,
        'personnels_types_with_available':personnels_types_with_available,
        'personnel_needs':personnel_needs,
        'facility_needs':facility_needs,
        'slug':slug,
        'needs_assessment':needs_assessment,
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
        needs_assessment.sector = sector
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
        needs = needs_assessment.needs.all()
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
    population_projections = PopulationProjection.objects.filter(user=request.user).all()
    needs_assessment = NeedsAssessment.objects.get(slug=slug)
    context = get_needs_assessment_context(slug=slug, request=request)
    if needs_type == 'personnel':
        personnel_needs = needs_assessment.needs.filter(needs_type='personnel')
        context['personnel_needs'] = personnel_needs
        context['needs_type'] = 'personnel'
        
    elif needs_type == 'facility':
        facility_needs = needs_assessment.needs.filter(needs_type='facility')
        context['facility_needs'] = facility_needs
        context['needs_type'] = 'facility'

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
            dashboard_template = get_template('partials/dashboard_main.html').render(context)
            return JsonResponse({'template':dashboard_template})
        return JsonResponse({'template': needs_assessment_template}, status=200)
    except (NeedsAssessment.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid request'}, status=400)


# delete needs assessment view
def delete_needs_assessment(request, slug):
    if request.method == 'DELETE':
        needs_assessment = NeedsAssessment.objects.get(slug=slug)
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
        dashboard_template = get_template('partials/dashboard_main.html').render(context)
        return JsonResponse({'template':dashboard_template})
    
    child_template = get_template('prms/needs_assessment.html').render(context)

    return render(request, 'prms/dashboard.html', {'child_template': child_template}) 
    


# needs assessment view
@csrf_exempt
def needs_assessment(request, slug=None):
    population_projections = PopulationProjection.objects.filter(user=request.user).all()
    if request.method == 'POST' and slug is None:
        return create_needs_assesment(request)
    elif slug is not None:
        if request.method == 'GET':
            return get_needs_assessment(request, slug)
        elif request.method == 'PUT':
            return update_needs_assessment(request, slug)
        elif request.method == 'DELETE':
            return delete_needs_assessment(request, slug)


    child_template = get_template('prms/needs_assessment.html').render({'population_projections':population_projections})
    if request.htmx:
        return render(request, 'prms/needs_assessment.html', {'population_projections':population_projections,})
    return render(request, 'prms/dashboard.html', {'child_template': child_template})    