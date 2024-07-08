from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Organisation

class UserOrganisationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register')
        self.create_org_url = reverse('create-organisation')
        self.login_url = reverse('login')
        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        # Register the user and store the access token for authenticated requests
        self.register_user()

    def register_user(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.token = response.data['data']['accessToken']

    def authenticate(self):
        print("Token:", self.token)
        # Set Authorization header with access token for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        print("Authentication Header:", self.client._credentials)

    def test_user_login(self):
        # Register the user first
        self.client.post(self.registration_url, self.user_data, format='json')
        # Now attempt to login
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])

    def test_get_organisations(self):
        self.authenticate()  # Ensure client is authenticated
        # Create some organizations for the user
        org1 = Organisation.objects.create(name="Org1", description="Organization 1")
        org2 = Organisation.objects.create(name="Org2", description="Organization 2")
        # User should be able to access their organizations
        response = self.client.get(reverse('organisations'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['organisations']), 2)  # Assuming user has 2 organizations

    def test_create_organisation(self):
        self.authenticate()  # Ensure client is authenticated
        new_org_data = {
            "name": "New Org",
            "description": "New Organization"
        }
        response = self.client.post(self.create_org_url, new_org_data, format='json')
        print("Create Organisation Response Data:", response.data)  # Debugging statement
        print("Create Organisation Response Status:", response.status_code)  # Debugging statement
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the created organization details in the response
        self.assertEqual(response.data['data']['name'], new_org_data['name'])
        self.assertEqual(response.data['data']['description'], new_org_data['description'])


    # Additional tests for other endpoints as needed

