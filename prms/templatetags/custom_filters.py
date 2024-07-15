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


# get distinct needs type
@register.filter(name='get_distinct_needs_type')
def get_distinct_needs_type(needs, needs_type):
    # filter needs
    if type(needs) == list:
        needs = [need for need in needs if need.needs_type == needs_type]
        return list(set([need.content_object.type_name for need in needs]))
    else:
        needs  = needs.filter(needs_type=needs_type)
        needs = [need.content_object.type_name for need in needs]
        return list(set(needs))
    
@register.filter(name='get_needs')
def get_needs(needs, needs_type):
    return needs.filter(needs_type=needs_type)


# range filter
@register.filter(name='in_range')
def in_range(value):
    return range(value)


@register.filter(name='get_needs_type')
def get_needs_type(needs):
    # get distinct needs type
    return list(set([need.needs_type for need in needs]))