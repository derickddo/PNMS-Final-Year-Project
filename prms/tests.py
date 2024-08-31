from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from prms.models import PopulationProjection, Region, District, Projection, User
from django.contrib.contenttypes.models import ContentType

class PopulationProjectionTests(TestCase):
    
    def setUp(self):
        # Set up initial data for testing
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a region and district for testing
        self.region = Region.objects.create(name='Test Region')
        self.district = District.objects.create(name='Test District', region=self.region)
        
        self.url = reverse('create_or_update_population_projection ')

    def test_create_population_projection_region(self):
        data = {
            'areaType': 'region',
            'title': 'Test Projection Region',
            'baseYearPopulation': '100000',
            'baseYear': '2020',
            'growthRate': '2.5',
            'projectYear': '2030',
            'description': 'Test Description',
            'growthRateType': 'manual',
            'slug': 'test-projection-region',
            'region': self.region.name
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        
        # Check if the population projection was created
        projection = PopulationProjection.objects.get(slug='test-projection-region')
        self.assertEqual(projection.title, 'Test Projection Region')
        self.assertEqual(projection.growth_rate, '2.5')
        self.assertEqual(projection.content_object, self.region)
        
        # Check projections were created
        self.assertTrue(projection.projections.exists())

    def test_create_population_projection_district(self):
        data = {
            'areaType': 'district',
            'title': 'Test Projection District',
            'baseYearPopulation': '50000',
            'baseYear': '2020',
            'growthRate': '3.0',
            'projectYear': '2030',
            'description': 'Test District Description',
            'growthRateType': 'manual',
            'slug': 'test-projection-district',
            'district': self.district.name
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        
        # Check if the population projection was created
        projection = PopulationProjection.objects.get(slug='test-projection-district')
        self.assertEqual(projection.title, 'Test Projection District')
        self.assertEqual(projection.growth_rate, '3.0')
        self.assertEqual(projection.content_object, self.district)
        
        # Check projections were created
        self.assertTrue(projection.projections.exists())

    def test_update_population_projection(self):
        # First create a population projection to update
        initial_data = {
            'areaType': 'region',
            'title': 'Initial Projection',
            'baseYearPopulation': '100000',
            'baseYear': '2020',
            'growthRate': '2.5',
            'projectYear': '2030',
            'description': 'Initial Description',
            'growthRateType': 'manual',
            'slug': 'initial-projection',
            'region': self.region.name
        }
        self.client.post(self.url, data=initial_data)
        projection = PopulationProjection.objects.get(slug='initial-projection')
        
        update_data = {
            'id': projection.id,
            'areaType': 'region',
            'title': 'Updated Projection',
            'baseYearPopulation': '120000',
            'baseYear': '2021',
            'growthRate': '3.5',
            'projectYear': '2035',
            'description': 'Updated Description',
            'growthRateType': 'manual',
            'slug': 'updated-projection',
            'region': self.region.name
        }
        response = self.client.put(self.url, data=update_data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        
        # Check if the population projection was updated
        projection.refresh_from_db()
        self.assertEqual(projection.title, 'Updated Projection')
        self.assertEqual(projection.growth_rate, '3.5')
        self.assertEqual(projection.description, 'Updated Description')
        self.assertTrue(projection.projections.exists())
    
    def test_create_population_projection_auto_growth_rate(self):
        # Assuming `get_growth_rate` is mocked to return a specific value
        data = {
            'areaType': 'region',
            'title': 'Auto Growth Rate Projection',
            'baseYearPopulation': '100000',
            'baseYear': '2020',
            'projectYear': '2030',
            'description': 'Test Description for Auto Growth Rate',
            'growthRateType': 'auto',
            'slug': 'auto-growth-rate-projection',
            'region': self.region.name
        }
        with patch('prms.views.get_growth_rate', return_value=2.0):
            response = self.client.post(self.url, data=data)
            self.assertEqual(response.status_code, 200)
            
            projection = PopulationProjection.objects.get(slug='auto-growth-rate-projection')
            self.assertEqual(projection.growth_rate, 2.0)
            self.assertTrue(projection.projections.exists())

