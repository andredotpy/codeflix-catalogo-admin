import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:
    def test_update_category_name(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(
            id=category_filme.id, name='Filme Documental'
        )
        use_case.execute(request)

        updated_category_filme = repository.get_by_id(id=category_filme.id)
        assert updated_category_filme.name == 'Filme Documental'  # type: ignore
        assert updated_category_filme.description == 'Descrição para filmes'  # type: ignore

    def test_update_category_description(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(
            id=category_filme.id,
            description='Descrição para filmes documentais',
        )
        use_case.execute(request)

        updated_category_filme = repository.get_by_id(id=category_filme.id)
        assert updated_category_filme.name == 'Filme'  # type: ignore
        assert (
            updated_category_filme.description  # type: ignore
            == 'Descrição para filmes documentais'
        )

    def test_update_category_activation(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes', is_active=False
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(id=category_filme.id, is_active=True)
        use_case.execute(request)

        updated_category_filme = repository.get_by_id(id=category_filme.id)
        assert updated_category_filme.is_active is True  # type: ignore

    def test_update_category_deactivation(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes', is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(id=category_filme.id, is_active=False)
        use_case.execute(request)

        updated_category_filme = repository.get_by_id(id=category_filme.id)
        assert updated_category_filme.is_active is False  # type: ignore

    def test_trying_to_update_category_with_not_found_id(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        use_case = UpdateCategory(repository)
        not_found_id = uuid.uuid4()
        request = UpdateCategoryRequest(
            id=not_found_id, name='Filme Documental'
        )
        with pytest.raises(
            CategoryNotFound, match=f'Category with id: {request.id} not found!'
        ):
            use_case.execute(request)

        not_updated_category_filme = repository.get_by_id(id=category_filme.id)
        assert not_updated_category_filme.name == 'Filme'  # type: ignore
        assert not_updated_category_filme.description == 'Descrição para filmes'  # type: ignore

    def test_update_category_with_invalid_name(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(id=category_filme.id, name='F' * 256)

        with pytest.raises(ValueError, match='name cannot be longer than 255'):
            use_case.execute(request)

        not_updated_category_filme = repository.get_by_id(id=category_filme.id)
        assert not_updated_category_filme.name == 'Filme'  # type: ignore
        assert not_updated_category_filme.description == 'Descrição para filmes'  # type: ignore
