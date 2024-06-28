from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Region, District, PopulationProjection, Projection, Population
import json
from django.views.decorators.csrf import csrf_exempt
from .population_projection_methods import calculate_projections, calculate_growth_rate
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
    
    

    context = {
        'population_projections':population_projections,
        # 'projections':projections,
        # 'base_years':base_years,
        # 'projection_years':projection_years
    }
    
    if request.htmx:
            return render(request, 'partials/dashboard_main.html', context)
    return render(request, 'prms/dashboard.html', context)

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

def generate_unique_slug(model, base_slug):
    unique_slug = base_slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    return unique_slug
def get_growth_rate(area_type, region, 
                district, 
                growth_rate_type, 
                growth_rate_manual):
    growth_rate = 0.0
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
    
    contex = {
        'population_projection' :population_projection,
        'projection_years':projection_years,
        'base_years':base_years,
        'projected_populations':projected_populations,
        'base_populations':base_populations,
        'range':custom_range,
        'growth_rate': format(population_projection.growth_rate, '.2f'),
        'id': population_projection.pk,
        'diff_year':diff_year
    }

    # Render the child template
    child_template = get_template('prms/population_projection.html').render(contex)
    

    # Check if the request is an htmx request
    if request.htmx:
        return render(request, 'prms/population_projection.html', contex)
    
    
    # If the request is not an htmx request, render the dashboard template
    return render(request, 'prms/dashboard.html', {'child_template': child_template})


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

def get_delete_template(request):
    template = get_template('partials/delete.html').render()
    
    if request.htmx:
        return render(request, 'partials/delete.html')
    return JsonResponse({'html':template})

def get_population_projection_form(request):
    template = get_template('forms/create_population_projection.html').render()
    return JsonResponse({'form_template':template})


def needs_assessment(request):
    population_projections = PopulationProjection.objects.all()
    if request.method == 'POST':
        projected_population_id = request.POST.get('projected_population')
        sector = request.POST.get('sector')
        projected_population = get_object_or_404(PopulationProjection, id=projected_population_id)

        base_population = projected_population.base_population
        projected_population_value = projected_population.projected_population

        # Calculate required, new need, and surplus
        standard_population = {
            'health': 5000,
            'education': 6000,
            'utility': 7000,
        }

        threshold = standard_population.get(sector, 5000)
        required = projected_population_value // threshold
        available = base_population // threshold
        new_need = required - available if required > available else 0
        surplus = available - required if available > required else 0

        result = {
            'required': required,
            'available': available,
            'new_need': new_need,
            'surplus': surplus,
        }

        return JsonResponse(result)

    child_template = get_template('prms/needs_assessment.html').render({'population_projections':population_projections})
    if request.htmx:
        return render(request, 'prms/needs_assessment.html', {'population_projections':population_projections})
    return render(request, 'prms/dashboard.html', {'child_template': child_template,})    