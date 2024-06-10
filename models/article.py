
from models.conn import conn, cursor

class Article:
    def __init__(self, title, content, author_id, magazine_id,id = None):
        if not isinstance(title,str):
            raise TypeError("Title must be a string")
        if not 5<= len(title)<=50:
            raise ValueError("Title must be between 5 and 50 characters")

        self.id = id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create_table(cls):
        cursor.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author_id INTEGER, magazine_id INTEGER, FOREIGN KEY (author_id) REFERENCES authors(id), FOREIGN KEY (magazine_id) REFERENCES magazines(id))")
        conn.commit()

    @classmethod
    def drop_table(cls):
        cursor.execute("DROP TABLE IF EXISTS articles")
        conn.commit()
        
    @property
    def title(self):
        return self._title

    def save(self):
        sql = "INSERT INTO articles(title,content,author_id,magazine_id)VALUES(?,?,?,?)"
        cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        conn.commit()
        self.id = CURSOR2.lastrowid

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
    # Check if author_id exists
        cursor.execute("SELECT COUNT(*) FROM authors WHERE id = ?", (author_id,))
        author_exists = cursor.fetchone()[0] > 0

    # Check if magazine_id exists
        cursor.execute("SELECT COUNT(*) FROM magazines WHERE id = ?", (magazine_id,))
        magazine_exists = cursor.fetchone()[0] > 0

        if not author_exists:
            raise ValueError("Author with id {} does not exist".format(author_id))

        if not magazine_exists:
            raise ValueError("Magazine with id {} does not exist".format(magazine_id))

        article = cls(title, content, author_id, magazine_id)
        article.save()
        return article

    def author(self):
        sql = "SELECT authors.name FROM articles INNER JOIN authors ON articles.author_id = authors.id WHERE articles.id = ?"
        cursor.execute(sql, (self.id,))
        return cursor.fetchone()[0]


    def magazine(self):
        sql = "SELECT magazines.name FROM articles INNER JOIN magazines ON articles.magazine_id = magazines.id WHERE articles.id = ?"
        cursor.execute(sql, (self.id,))
        return cursor.fetchone()[0]


    def __repr__(self):
        return f'<Article {self.title}>'
