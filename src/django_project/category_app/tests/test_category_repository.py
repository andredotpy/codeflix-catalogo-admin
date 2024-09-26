import uuid

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django_project.category_app.models import Category as CategoryModel

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import (
    DjangoORMCategoryRepository,
)


@pytest.mark.django_db
class TestSave:
    def test_save_new_category_in_db(self):
        category = Category(name='Filme', description='Descrição de filmes.')
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category=category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active


@pytest.mark.django_db
class TestGetById:
    def test_get_category_by_id_in_db(self):
        category = Category(name='Filme', description='Descrição de filmes.')
        repository = DjangoORMCategoryRepository()
        repository.save(category=category)

        get_category = CategoryModel.objects.get(id=category.id)

        assert get_category is not None
        assert get_category.name == 'Filme'
        assert get_category.description == 'Descrição de filmes.'
        assert get_category.is_active is True

    def test_get_category_by_not_found_id_in_db(self):
        category = Category(name='Filme', description='Descrição de filmes.')
        repository = DjangoORMCategoryRepository()
        repository.save(category=category)

        not_found_id = uuid.uuid4()

        with pytest.raises(ObjectDoesNotExist):
            CategoryModel.objects.get(id=not_found_id)


@pytest.mark.django_db
class TestDelete:
    def test_delete_category_in_db(self):
        category = Category(name='Filme', description='Descrição de filmes.')
        repository = DjangoORMCategoryRepository()
        repository.save(category=category)

        assert CategoryModel.objects.count() == 1

        repository.delete(id=category.id)
        assert CategoryModel.objects.count() == 0
