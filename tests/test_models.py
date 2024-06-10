import unittest
from models.author import Author
from models.article import Article
from models.conn import conn,cursor
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article("Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine("WL Africa", "Category")
        self.assertEqual(magazine.name, "WL Africa")

    def test_author_name_type(self):
        author = Author("John Doe")
        self.assertIsInstance(author.name, str)

    def test_author_name_length(self):
        author = Author("John Doe")
        self.assertGreater(len(author.name), 0)

    def test_magazine_name_type(self):
        magazine = Magazine("WL Africa", "Category")
        self.assertIsInstance(magazine.name, str)

    def test_magazine_name_length(self):
        with self.assertRaises(ValueError):
            magazine_short_name = Magazine("M", "Category")

        magazine_valid_name = Magazine("Valid Name", "Category")
        self.assertEqual(magazine_valid_name.name, "Valid Name")

        with self.assertRaises(ValueError):
            magazine_long_name = Magazine("This is a long name", "Category")

    def test_category_name(self):
        # Add your test logic here
        pass

if __name__ == "__main__":
    unittest.main()
