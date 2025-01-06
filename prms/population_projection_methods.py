facility_standards = {
    'hospital': 200000,
    'health center':25000,
    'clinic':5000,
    'chps': 5000
}

personnel_standards = {
    'doctor': 5000,
    'nurse': 5000,
    'midwife': 5000,
    'pharmacist': 5000,
    'lab technician': 5000,
}

classroom_standards = {
    'primary': 40,
    'jhs': 40,
    'pre-school': 40,
    'shs': 40,
    'tertiary': 40
}

dual_desk_standards = {
    'primary': 2,
    'jhs': 2,
    'pre-school': 2,
    'shs': 2,
    'tertiary': 2
}

water_source_standards = {
    'borehole': 300,
    'pipe': 300,
    'well': 300,
}

toilet_standards = {
    'public': 5000,
    # 1 per household for private
    'private': 1
}

skip_container_standards = {
    'public': 5000,
    # 1 per household for private
    'private': 1
}


# Description: Population projection methods
def linear(year, next_year, current_population, growth_rate):
       t = next_year - year
       # covert growth rate
       growth_rate = growth_rate / 100
       return current_population * ((1 + (growth_rate * t)) ** t)
       
def calculate_projections(base_year, projecting_year, base_population, growth_rate):
        """ Calculate population projections """
        results = []
        current_population = base_population

        for year in range(base_year, projecting_year):
            next_year = year + 1
            projected_population = linear(year, next_year, current_population, growth_rate)
            results.append({
                'base_year': year,
                'base_population': int(current_population),
                'projecting_year': next_year,
                'projected_population': int(projected_population)
            })
            current_population = projected_population

        return results

def calculate_growth_rate(pop_2010, pop_2021) -> float:
        """ Calculate the growth rate """
        years_between = 2021 - 2010
        
        growth_rate = float(((pop_2021 / pop_2010) ** (1 / years_between) - 1) * 100)
        print(pop_2021, pop_2010, growth_rate)
        return growth_rate
        

def calculate_facilities_required(population,facility_numbers,year, standards=facility_standards):
    
        """ Calculate the number of facilities required """
        results = []
        for facility_type, available in facility_numbers.items():
            standard = standards[str(facility_type).lower()]
            required_facilities = int(population / standard)
            temp = int(available) - int(required_facilities) 
            suplus = None
            new_need = None
            
            # check if new need is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if new need is negative then there is no suplus and there is new need
                new_need = abs(temp)
            
            results.append({
                'year':year,
                'facility_type':facility_type,
                'available':available,
                'required':required_facilities,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })

        return results

def calculate_personnel_required(population, personnel_numbers, year, standards=personnel_standards):
        """ Calculate the number of personnel required """
        results = []
        for personnel_type, available in personnel_numbers.items():
            standard = standards[str(personnel_type).lower()]
            required_personnel = int(population / standard)
            temp =  int(available) - int(required_personnel)
            suplus = None
            new_need = None
            
            # check if new need is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if new need is negative then there is no suplus and there is new need
                # convert to positive
                new_need = abs(temp)
            
            results.append({
                'year':year,
                'personnel_type':personnel_type,
                'available':available,
                'required':required_personnel,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })

        return results

def calculate_classrooms_required(population, classroom_numbers, year, standards=classroom_standards):
        """ Calculate the number of classrooms required """
        results = []
        for classroom_type, available in dict(classroom_numbers).items():
            standard = standards[classroom_type.lower()]
            required_classrooms = int(population / standard)
            temp = int(available) - int(required_classrooms)
            suplus = None
            new_need = None
            
            # check if temp is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if temp is negative then there is no suplus and there is new need
                new_need = abs(temp)
            
            
            results.append({
                'year':year,
                'classroom_type':classroom_type,
                'available':available,
                'required':required_classrooms,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })

        return results

def calculate_dual_desks_required(population, dual_desk_numbers, year, standards=dual_desk_standards):
        """ Calculate the number of dual desks required """
        results = []
        for dual_desk_type, available in dual_desk_numbers.items():
            standard = standards[dual_desk_type.lower()]
            required_desks = int(population / standard)
            temp = int(available) - int(required_desks)
            suplus = None
            new_need = None

            # check if temp is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if temp is negative then there is no suplus and there is new need
                new_need = abs(temp)

            
            results.append({
                'year':year,
                'dual_desk_type':dual_desk_type,
                'available':available,
                'required':required_desks,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })

        return results

def calculate_water_sources_required(population, water_source_numbers, year, standards=water_source_standards):
        """ Calculate the number of water sources required """
        results = []
        for water_source_type, available in water_source_numbers.items():
            standard = standards[water_source_type.lower()]
            required_sources = int(population / standard)
            temp = int(available) - int(required_sources)
            suplus = None
            new_need = None

            # check if temp is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if temp is negative then there is no suplus and there is new need
                new_need = abs(temp)
            
            
            results.append({
                'year':year,
                'water_source_type':water_source_type,
                'available':available,
                'required':required_sources,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })
        return results

def calculate_toilets_required(population, toilet_numbers, year, standards=toilet_standards):
        """ Calculate the number of toilets required """
        results = []
        for toilet_type, available in toilet_numbers.items():
            standard = standards[toilet_type.lower()]
            required_toilets = int(population / standard)
            temp = int(available) - int(required_toilets) 
            suplus = None
            new_need = None

            # check if temp is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if temp is negative then there is no suplus and there is new need
                new_need = abs(temp)
            
            
            results.append({
                'year':year,
                'toilet_type':toilet_type,
                'available':available,
                'required':required_toilets,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })
        return results

def calculate_skip_containers_required(population, skip_container_numbers, year, standards=skip_container_standards):
        """ Calculate the number of skip containers required """
        results = []
        for skip_container_type, available in skip_container_numbers.items():
            standard = standards[skip_container_type.lower()]
            required_skip_containers = int(population / standard)
            temp = int(available) - int(required_skip_containers)
            suplus = None
            new_need = None

            # check if temp is positive then there is suplus
            if temp > 0:
                suplus = temp
            else:
                # check if temp is negative then there is no suplus and there is new need
                new_need = abs(temp)
            
            
            results.append({
                'year':year,
                'skip_container_type':skip_container_type,
                'available':available,
                'required':required_skip_containers,
                'standard': standard,
                'new_need': new_need,
                'suplus':suplus,
                'population':population
            })
        return results