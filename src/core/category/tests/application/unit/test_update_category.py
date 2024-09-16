from unittest.mock import create_autospec

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(name='Filme', description='Descrição para filmes')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name='Série',
        )
        use_case.execute(request)

        assert category.name == 'Série'
        assert category.description == 'Descrição para filmes'
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(name='Filme', description='Descrição para filmes')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description='Nova descrição para filmes',
        )
        use_case.execute(request)

        assert category.name == 'Filme'
        assert category.description == 'Nova descrição para filmes'
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(name='Filme', description='Descrição para filmes')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=False)

        assert category.is_active is True
        use_case.execute(request)

        assert category.name == 'Filme'
        assert category.description == 'Descrição para filmes'
        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            name='Filme', description='Descrição para filmes', is_active=False
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=True)

        assert category.is_active is False
        use_case.execute(request)

        assert category.name == 'Filme'
        assert category.description == 'Descrição para filmes'
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)
