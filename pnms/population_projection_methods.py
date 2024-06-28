# Description: Population projection methods
def linear(year, next_year, current_population, growth_rate):
       t = next_year - year
       return current_population * (1 + (growth_rate * t))
       
def calculate_projections(base_year, projecting_year, base_population, growth_rate):
        """ Calculate population projections """
        results = []
        current_population = base_population

        for year in range(base_year, projecting_year):
            next_year = year + 1
            projected_population = linear(year, next_year, current_population, growth_rate)
            results.append({
                'base_year': year,
                'base_population': current_population,
                'projecting_year': next_year,
                'projected_population': projected_population
            })
            current_population = projected_population

        return results

def calculate_growth_rate(pop_2010, pop_2021) -> float:
        """ Calculate the growth rate """
        t = 2021 - 2010
        return  float((int(pop_2021) - int(pop_2010)) / (pop_2010 * t))