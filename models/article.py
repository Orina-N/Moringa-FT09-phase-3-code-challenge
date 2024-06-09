from conn2 import CONN2, CURSOR2

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
        CURSOR2.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author_id INTEGER, magazine_id INTEGER, FOREIGN KEY (author_id) REFERENCES authors(id), FOREIGN KEY (magazine_id) REFERENCES magazines(id))")
        CONN2.commit()

    @classmethod
    def drop_table(cls):
        CURSOR2.execute("DROP TABLE IF EXISTS articles")
        CONN2.commit()
        
    @property
    def title(self):
        return self._title

    def save(self):
        sql = "INSERT INTO articles(title,content,author_id,magazine_id)VALUES(?,?,?,?)"
        CURSOR2.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        CONN2.commit()
        self.id = CURSOR2.lastrowid

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
    # Check if author_id exists
        CURSOR2.execute("SELECT COUNT(*) FROM authors WHERE id = ?", (author_id,))
        author_exists = CURSOR2.fetchone()[0] > 0

    # Check if magazine_id exists
        CURSOR2.execute("SELECT COUNT(*) FROM magazines WHERE id = ?", (magazine_id,))
        magazine_exists = CURSOR2.fetchone()[0] > 0

        if not author_exists:
            raise ValueError("Author with id {} does not exist".format(author_id))

        if not magazine_exists:
            raise ValueError("Magazine with id {} does not exist".format(magazine_id))

        article = cls(title, content, author_id, magazine_id)
        article.save()
        return article

    def author(self):
        sql = "SELECT authors.name FROM articles INNER JOIN authors ON articles.author_id = authors.id WHERE articles.id = ?"
        CURSOR2.execute(sql, (self.id,))
        return CURSOR2.fetchone()[0]


    def magazine(self):
        sql = "SELECT magazines.name FROM articles INNER JOIN magazines ON articles.magazine_id = magazines.id WHERE articles.id = ?"
        CURSOR2.execute(sql, (self.id,))
        return CURSOR2.fetchone()[0]


    def __repr__(self):
        return f'<Article {self.title}>'

article_3 = Article.create("Man Eaters","THE 2 lions of Tsavo",4,1)
