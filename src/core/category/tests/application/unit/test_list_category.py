from unittest.mock import MagicMock

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from src.core.category.domain.category import Category


class TestListCategory:
    def test_list_category(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        category_serie = Category(
            name='Série', description='Descrição para séries'
        )
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.list.return_value = [category_filme, category_serie]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active,
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active,
                ),
            ]
        )

    def test_list_category_with_empty_repository(self):
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])
