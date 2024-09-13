from uuid import UUID

import pytest

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from src.core.category.application.use_cases.exceptions import InvalidCategoryInput
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreatecategory:
    def test_create_category_with_valid_input(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository)
        request = CreateCategoryRequest(
            name='Filme',
            description='Descrição para filmes',
            is_active=False,
        )

        category_response = use_case.execute(request)
        assert category_response is not None
        assert isinstance(category_response, CreateCategoryResponse)
        assert isinstance(category_response.id, UUID)

        assert len(repository.categories) == 1

        new_category_registry = repository.categories[0]
        assert new_category_registry.id == category_response.id
        assert new_category_registry.name == 'Filme'
        assert new_category_registry.description == 'Descrição para filmes'
        assert new_category_registry.is_active is False

    def test_create_category_with_invalid_input(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository)
        request = CreateCategoryRequest(name='')

        with pytest.raises(InvalidCategoryInput, match='name cannot be empty'):
            use_case.execute(request)
