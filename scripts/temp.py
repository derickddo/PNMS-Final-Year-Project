def linear(base_year, projecting_year, population, growth_rate):
        return population + (projecting_year - base_year) * growth_rate


def calculate_projections(base_year, projecting_year, population, growth_rate):
    results = []
    current_population = population

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

temp = calculate_projections(2021, 2025, 1000, 14)
print(temp)