from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = '/api/categories/'
        response = self.client.get(url)
        expected_data = [
            {
                'id': 'b23r-asfdo',
                'name': 'movie',
                'description': 'descriçao de movie',
                'is_active': True,
            }
        ]

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
