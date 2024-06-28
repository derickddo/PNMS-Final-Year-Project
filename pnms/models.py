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

    def __str__(self):
        return f'Needs assestment for {self.sector} sector in {self.population_projection.area_type}'  
    class Meta:
        db_table = 'needs_assestment'

class MapPrediction(models.Model):
    population_projection = models.ForeignKey(PopulationProjection, on_delete=models.CASCADE)
    needs_assestment = models.ForeignKey(NeedsAssessment, on_delete=models.CASCADE)
    map_url = models.URLField()
    description = models.TextField()

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
