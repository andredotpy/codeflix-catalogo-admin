import uuid

import pytest

from category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            category = Category()  # noqa

    def test_empt_name_string(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            category = Category(name='')  # noqa

    def test_name_must_have_less_than_256_characteres(self):
        with pytest.raises(ValueError, match='name cannot be longer than 255'):
            Category(name='a' * 256)

    def test_category_id_must_be_uuid(self):
        category = Category(name='movie')
        assert isinstance(category.id, uuid.UUID)

    def test_create_category_with_default_values(self):
        category = Category(name='movie')
        assert category.name == 'movie'
        assert category.description == ''
        assert category.is_active is True

    def test_create_category_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name='movie',
            description='movie description',
            is_active=False,
        )
        assert category.id == category_id
        assert category.name == 'movie'
        assert category.description == 'movie description'
        assert category.is_active is False

    def test_category_str(self):
        category = Category(name='movie')
        assert category.__str__() == '<Category: movie -  (True)>'

    def test_category_repr(self):
        category_id = uuid.uuid4()
        category = Category(id=category_id, name='movie')
        assert category.__repr__() == f'<Category: {category_id}::movie>'


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name='filme', description='categoria para filmes')
        category.update_category(
            name='documentário', description='categoria para documentários'
        )
        assert category.name == 'documentário'
        assert category.description == 'categoria para documentários'

    def test_update_category_with_invalid_name(self):
        category = Category(name='filme', description='categoria para filmes')
        with pytest.raises(ValueError, match='name cannot be longer than 255'):
            category.update_category(
                name='a' * 256, description='categoria para name inválido'
            )

    def test_update_category_with_empty_name_string(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            category = Category(name='')  # noqa


class TestActivateCategory:
    def test_activate_inactive_category(self):
        category = Category(
            name='Filme', description='descrição para filmes', is_active=False
        )
        category.activate()
        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(
            name='Filme', description='descrição para filmes', is_active=True
        )
        category.activate()
        assert category.is_active is True


class TestDeactivateCategory:
    def test_deactivate_inactive_category(self):
        category = Category(
            name='Filme', description='descrição para filmes', is_active=False
        )
        category.deactivate()
        assert category.is_active is False

    def test_deactivate_active_category(self):
        category = Category(
            name='Filme', description='descrição para filmes', is_active=True
        )
        category.deactivate()
        assert category.is_active is False


class TestEqualityCategory:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(
            name='Filme', description='Descrição para filmes', id=common_id
        )
        category_2 = Category(
            name='Filme', description='Descrição para filmes', id=common_id
        )
        assert category_1 == category_2

    def test_equality_with_different_classes(self):
        class Dummy:
            def __init__(self, id) -> None:
                self.id = id

        common_id = uuid.uuid4()
        category = Category(
            name='Filme', description='Descrição para filmes', id=common_id
        )
        dummy = Dummy(id=common_id)
        assert category != dummy
