import uuid

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import (
    DjangoORMCategoryRepository,
)


@pytest.fixture
def category_filme() -> Category:
    return Category(name='Filme', description='Categoria de filmes.')


@pytest.fixture
def category_serie() -> Category:
    return Category(name='Série', description='Categoria de séries.')


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListCategoryAPI:
    def test_list_categories(
        self,
        category_filme: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_filme)
        category_repository.save(category_serie)

        url = '/api/categories/'
        response = APIClient().get(url)
        expected_data = {
            'data': [
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
        }
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestGetCategoryAPI:
    def test_return_category_if_it_exists(
        self,
        category_filme: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_filme)

        url = '/api/categories/{category_id}/'.format(
            category_id=str(category_filme.id)
        )
        response = APIClient().get(url)

        expected_data = {
            'data': {
                'id': str(category_filme.id),
                'name': 'Filme',
                'description': 'Categoria de filmes.',
                'is_active': True,
            }
        }

        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_if_category_does_not_exist(
        self,
        category_filme: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_filme)

        id_that_does_not_exist = uuid.uuid4()

        url = '/api/categories/{category_id}/'.format(
            category_id=str(id_that_does_not_exist)
        )
        response = APIClient().get(url)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_return_400_if_id_is_invalid(
        self,
        category_filme: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_filme)

        invalid_id = '1234'

        url = '/api/categories/{category_id}/'.format(
            category_id=str(invalid_id)
        )
        response = APIClient().get(url)

        assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCreateCategoryAPI:
    def test_create_category(
        self, category_repository: DjangoORMCategoryRepository
    ):
        url = '/api/categories/'
        data = {
            'name': 'Filme',
            'description': 'Categoria para filmes.',
        }
        response = APIClient().post(url, data=data)
        created_category_id = uuid.UUID(response.data['id'])

        assert response.status_code == HTTP_201_CREATED
        assert category_repository.get_by_id(
            id=created_category_id
        ) == Category(
            id=created_category_id,
            name='Filme',
            description='Categoria para filmes.',
            is_active=True,
        )

    def test_create_category_with_invalid_payload_no_name(self):
        url = '/api/categories/'
        data = {
            'name': '',
            'description': 'Categoria com nome vazio não pode.',
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_create_category_with_invalid_payload_name_to_long(self):
        url = '/api/categories/'
        data = {
            'name': 'a' * 256,
            'description': 'Nome não pode ter mais que 255 chars.',
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
