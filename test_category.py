import unittest
import uuid

from category import Category

class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaises(TypeError):
            Category()

    def test_name_must_have_less_than_256_characteres(self):
        with self.assertRaisesRegex(ValueError, "name must have less than 256 characteres"):
            Category(name="a"*256)

    def test_category_id_must_be_uuid(self):
        category = Category(name="movie")
        self.assertEqual(type(category.id), uuid. UUID)

    def test_create_category_with_default_values(self):
        category = Category(name="movie")
        self.assertEqual(category.name, "movie")
        self.assertEqual(category.description, "")
        self.assertEqual(category.is_active, True)

    def test_create_category_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id, name="movie", description="movie description", is_active=False
        )
        self.assertEqual(category.id, category_id)
        self.assertEqual(category.name, "movie")
        self.assertEqual(category.description, "movie description")
        self.assertEqual(category.is_active, False)

    def test_category_str(self):
        category = Category(name="movie")
        self.assertEqual(category.__str__(), "<Category: movie -  (True)>")

    def test_category_repr(self):
        category_id = uuid.uuid4()
        category = Category(id=category_id, name="movie")
        self.assertEqual(category.__repr__(), f"<Category: {category_id}::movie>")

if __name__ == "__main__":
    unittest.main()
