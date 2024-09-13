import uuid
from unittest.mock import MagicMock

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_get_category_by_id(self):
        category = Category(name='Filme', description='Descrição para filmes')
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def test_get_category_by_id_with_not_found_id(self):
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound, match=f'Category with id: {request.id} not found!'):
            use_case.execute(request)
