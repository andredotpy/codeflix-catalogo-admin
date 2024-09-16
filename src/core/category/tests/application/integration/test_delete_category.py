import uuid

import pytest

from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        category_serie = Category(
            name='Série', description='Descrição para séries'
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        use_case = DeleteCategory(repository)
        request = DeleteCategoryRequest(id=category_filme.id)

        assert repository.get_by_id(category_filme.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(category_filme.id) is None
        assert response is None

    def test_delete_category_from_repository_with_not_found_id(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        category_serie = Category(
            name='Série', description='Descrição para séries'
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        use_case = DeleteCategory(repository)
        not_found_id = uuid.uuid4()
        request = DeleteCategoryRequest(id=not_found_id)

        assert repository.get_by_id(category_filme.id) is not None

        with pytest.raises(
            CategoryNotFound, match=f'Category with id: {request.id} not found!'
        ):
            use_case.execute(request)
