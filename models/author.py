
from models.conn import conn,cursor

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Author name must be longer than 0 characters ")
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("Author ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    def save(self):
        sql = """
        INSERT INTO authors (name) VALUES (?)
        """
        cursor.execute(sql, (self.name,))
        conn.commit()
        self.id = cursor.lastrowid

    @classmethod
    def create(cls, name):
        sql = "SELECT id FROM authors WHERE name = ?"
        cursor.execute(sql, (name,))
        result = cursor.fetchone()
        if result:
            author_id = result[0]
            return cls(name, id=author_id)
        else:
            author = cls(name)
            author.save()
            return author

    def articles(self):
        sql = """
         SELECT articles.title
         FROM articles
         WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        article_titles = [row[0] for row in cursor.fetchall()]
        return article_titles

    def magazines(self):
        sql = """
        SELECT DISTINCT magazines.name
        FROM articles
        INNER JOIN magazines ON articles.magazine_id = magazines.id
        WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        magazine_names = [row[0] for row in cursor.fetchall()]
        return magazine_names

    def __repr__(self):
        return f'<Author {self.name}>'


