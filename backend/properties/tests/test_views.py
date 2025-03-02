from django.test import TestCase
from django.urls import reverse

class PropertyViewTests(TestCase):
    def test_properties_endpoint_with_address(self):
        # Specify the query parameter
        response = self.client.get(reverse('property_view'), data={'address': '123 Main St'})
        
        # Check the response status
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = response.json()
        
        # Verify the response structure
        self.assertIn("normalized_address", data)
        self.assertIn("square_footage", data)
        self.assertIn("lot_size_acres", data)
        self.assertIn("year_built", data)
        self.assertIn("property_type", data)
        self.assertIn("bedrooms", data)
        self.assertIn("bathrooms", data)
        self.assertIn("room_count", data)
        self.assertIn("septic_system", data)
        self.assertIn("sale_price", data)
    
    def test_properties_endpoint_without_address(self):
        # Call the endpoint without query parameters
        response = self.client.get(reverse('property_view'))
        
        # Assert 400 response
        self.assertEqual(response.status_code, 400)
        
        # Verify error message
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Address is required')
