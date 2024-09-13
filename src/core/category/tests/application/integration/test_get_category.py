import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategoty:
    def test_get_category_by_id(self):
        category_filme = Category(name='Filme', description='Descrição para filmes')
        category_serie = Category(name='Série', description='Descrição para séries')
        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])

        use_case = GetCategory(repository)
        request = GetCategoryRequest(id=category_filme.id)

        response = use_case.execute(request)

        assert isinstance(response, GetCategoryResponse)
        assert response == GetCategoryResponse(
            id=category_filme.id,
            name=category_filme.name,
            description=category_filme.description,
            is_active=category_filme.is_active,
        )

    def test_get_category_by_id_with_not_found_id(self):
        category_filme = Category(name='Filme', description='Descrição para filmes')
        category_serie = Category(name='Série', description='Descrição para séries')
        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])

        use_case = GetCategory(repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
