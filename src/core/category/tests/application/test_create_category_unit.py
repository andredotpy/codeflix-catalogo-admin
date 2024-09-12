from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    InvalidCategoryInput,
)


class TestCreateCategory:
    def test_create_category_with_valid_input(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name='Filme',
            description='Descrição para filmes',
            is_active=False,
        )

        category_response = use_case.execute(request)

        assert category_response is not None
        assert isinstance(category_response.id, UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_input(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name='')

        with pytest.raises(InvalidCategoryInput, match='name cannot be empty'):
            use_case.execute(request)
