from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(default='avatar.png', null=True, blank=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'user'

class Population(models.Model):
    population = models.PositiveBigIntegerField()
    year = models.IntegerField()
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
 

    def __str__(self):
        return str(self.population)

    class Meta:
        db_table = 'population'


class Region(models.Model):
    name = models.CharField(max_length=30)
    map_url = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'region'

class District(models.Model):
    DISTRICTS_TYPE_CHOICES = [
        ('district', 'District'),
        ('municipal', 'Municipal'),
        ('metropolitan', 'Metropolitan')
    ]
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    map_url = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'district'

    
    

class PopulationProjection(models.Model):
    AREA_TYPE_CHOICES = [
        ('region', 'Region'),
        ('district', 'District'),
        ('town', 'Town')
    ]
    growth_rate = models.FloatField()
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    projections = models.ManyToManyField('Projection', related_name='projections')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        # generate title upon save
        if not self.title:
            self.title = f'Population projection for {self.content_object.name} {self.area_type}'
        super().save(*args, **kwargs) # Call the real save() method
    
    def delete(self, *args, **kwargs): # delete all projections when a population projection is deleted
        self.projections.clear()
        super().delete(*args, **kwargs) # Call the real delete() method
    

    class Meta:
        db_table = 'population_projection'


class NeedsAssessment(models.Model):
    SECTORS_CHOICES = [
        ('health', 'Health'),
        ('education', 'Education'),
        ('water', 'Water'),
        ('sanitation', 'Sanitation'),
    ]
    population_projection = models.ForeignKey(PopulationProjection, on_delete=models.CASCADE)
    sector = models.CharField(max_length=50, choices=SECTORS_CHOICES)
    needs = models.ManyToManyField('Needs', related_name='needs')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return f'Needs assessment for {self.sector} sector for a {self.population_projection.area_type}' 
    
    # delete all needs
    def delete(self, *args, **kwargs):
        for need in self.needs.all():
            need.delete()
        super().delete(*args, **kwargs)
     
    class Meta:
        db_table = 'needs_assessment'

class FacilityType(models.Model):
    type_name = models.CharField(max_length=50)
    year = models.IntegerField()
    standard = models.IntegerField()
    required = models.IntegerField()
    new_need = models.IntegerField(null=True, blank=True)
    suplus = models.IntegerField(null=True, blank=True)
    available = models.PositiveBigIntegerField(null=True, blank=True)
    population = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.type_name
    
    class Meta:
        db_table = 'facility_type'

class PersonnelType(models.Model):
    type_name = models.CharField(max_length=50)
    year = models.IntegerField()
    standard = models.IntegerField()
    required = models.IntegerField()
    new_need = models.IntegerField(null=True, blank=True)
    suplus = models.IntegerField(null=True, blank=True)
    available = models.PositiveBigIntegerField(null=True, blank=True)
    population = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.type_name
    
    class Meta:
        db_table = 'personnel_type'

class EquipmentType(models.Model):
    type_name = models.CharField(max_length=50)
    year = models.IntegerField()
    standard = models.IntegerField()
    required = models.IntegerField()
    new_need = models.IntegerField(null=True, blank=True)
    suplus = models.IntegerField(null=True, blank=True)
    available = models.PositiveBigIntegerField(null=True, blank=True)
    population = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.type_name
    
    class Meta:
        db_table = 'equipment_type'

class FurnitureType(models.Model):
    type_name = models.CharField(max_length=50)
    year = models.IntegerField()
    standard = models.IntegerField()
    required = models.IntegerField()
    new_need = models.IntegerField(null=True, blank=True)
    suplus = models.IntegerField(null=True, blank=True)
    available = models.PositiveBigIntegerField(null=True, blank=True)
    population = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.type_name
    

class OtherType(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Needs(models.Model):
    NEEDS_TYPE_CHOICES = [
        ('facility', 'Facility'),
        ('personnel', 'Personnel'),
        ('equipment', 'Equipment'),
        ('furniture', 'Furniture'),
        ('others', 'Others')
    ]
    needs_type = models.CharField(max_length=50, choices=NEEDS_TYPE_CHOICES, default='facility')
    # generic one to many relationship to all needs
    object_id = models.IntegerField() # id of the needs type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) # type of the needs
    content_object = GenericForeignKey('content_type', 'object_id') # the needs object
 
    def __str__(self):
        return f'needs for {self.needs_type}'

    def delete(self, *args, **kwargs):
        # delete all generic relations
        self.content_object.delete()
        self.content_type.delete()
        self.object_id.delete()
        super().delete(*args, **kwargs)  

    class Meta:
        db_table = 'needs'





class MapPrediction(models.Model):
    population_projection = models.ForeignKey(PopulationProjection, on_delete=models.CASCADE)
    needs_assestment = models.ForeignKey(NeedsAssessment, on_delete=models.CASCADE)
    map_url = models.URLField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Map prediction for {self.population_projection.area_type} '
    
    class Meta:
        db_table = 'map_prediction'

class Projection(models.Model):
    base_year = models.IntegerField()
    projecting_year = models.IntegerField()
    base_population = models.IntegerField()
    projected_population = models.IntegerField()

    def __str__(self):
        return f'{self.base_year} to {self.projecting_year}'
    class Meta:
        db_table = 'projection'
