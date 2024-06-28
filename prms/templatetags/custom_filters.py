from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    try:
        position = int(position)
        return sequence[position]
    except (IndexError, ValueError, TypeError):
        return None

@register.filter(name='queryset_to_list')
def queryset_to_list(queryset):
    return list(queryset)

@register.filter(name='get_base_years')
def get_base_years(projections):
    return [projection.base_year for projection in projections]

@register.filter(name='get_projected_population')
def get_projected_population(projections):
    return [projection.projected_population for projection in projections]
