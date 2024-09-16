from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestInMemoryCategoryRepository:
    def test_can_save_category_in_memory(self):
        repository = InMemoryCategoryRepository()
        category = Category(name='Filme', description='Descrição para filmes')

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_can_get_category_by_id_in_memory(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        category_serie = Category(
            name='Série', description='Descrição para séries'
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        category = repository.get_by_id(id=category_filme.id)

        assert category is not None
        assert category == category_filme

    def test_can_delete_category_in_memory(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        category_serie = Category(
            name='Série', description='Descrição para séries'
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )

        assert len(repository.categories) == 2
        category = repository.delete(id=category_filme.id)

        assert category is None
        assert len(repository.categories) == 1

    def test_can_update_category_in_memory(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        repository = InMemoryCategoryRepository(categories=[category_filme])

        category_filme.name = 'Novo filme'
        repository.update(category_filme)

        category = repository.get_by_id(id=category_filme.id)

        assert category.name == 'Novo filme'  # type: ignore
        assert category.description == 'Descrição para filmes'  # type: ignore

    def test_can_list_category_in_memory(self):
        category_filme = Category(
            name='Filme', description='Descrição para filmes'
        )
        category_serie = Category(
            name='Série', description='Descrição para séries'
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        response = repository.list()

        assert response == [category_filme, category_serie]
