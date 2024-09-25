from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category_filme = Category(
            name='Filme', description='Categoria de filmes.'
        )
        category_serie = Category(
            name='Série', description='Categoria de séries.'
        )
        repository = DjangoORMCategoryRepository()
        repository.save(category_filme)
        repository.save(category_serie)

        url = '/api/categories/'
        response = self.client.get(url)
        expected_data = [
            {
                'id': str(category_filme.id),
                'name': 'Filme',
                'description': 'Categoria de filmes.',
                'is_active': True,
            },
            {
                'id': str(category_serie.id),
                'name': 'Série',
                'description': 'Categoria de séries.',
                'is_active': True,
            },
        ]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)  # type: ignore
