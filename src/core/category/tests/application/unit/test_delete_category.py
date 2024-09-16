import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_by_id(self):
        category = Category(name='Filme', description='Descrição para filmes')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id)

    def test_delete_category_by_id_with_not_found_id(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(mock_repository)
        not_found_id = uuid.uuid4()
        request = DeleteCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound, match=f'Category with id: {request.id} not found!'):
            use_case.execute(request)

        mock_repository.delete.assert_not_called()
