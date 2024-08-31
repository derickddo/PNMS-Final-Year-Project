import json
from django.test import RequestFactory
from django.contrib.auth.models import User
from prms.models import PopulationProjection, Sector, NeedsAssessment
from prms.views import utility_needs_assessment
import json
from django.test import RequestFactory
from django.contrib.auth.models import User
from prms.models import PopulationProjection, Sector, NeedsAssessment, Region, District, MapPrediction, Population
from prms.views import create_needs_assesment
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='email@gmail.com'
        )
        self.user.set_password('12345')
        self.user.save()

        # Create a sector
        self.sector = Sector.objects.create(
            name='Test Sector',
            description='Test Description'
        )

        # Create a Region
        self.region = Region.objects.create(
            name='Test Region',
            description='Test Description'
        )

        # Create a District
        self.district = District.objects.create(
            name='Test District',
            description='Test Description',
            region=self.region
        )

        # Create a population projection
        self.population_projection = PopulationProjection.objects.create(
            growth_rate=0.5,
            area_type='Test Area Type',
            title='Test Title',
            slug='test-title',
            user=self.user
            content_type=ContentType.objects.get_for_model(Population),
            content_object = 
            object_id=1,
            is_education_enrollment=True
            
        )


        