from models.conn import conn, cursor

class Magazine:
    def __init__(self, name, category, id = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not 2 <= len(name) <= 16:
            raise ValueError("Names must be between 2 and 16 characters, inclusive")
        if not isinstance(category,str):
            raise TypeError("Category must be a string")
        if len(category) == 0:
            raise ValueError("Name cannot be empty")

        self._id = id
        self._name = name
        self._category = category


    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        CONSTRAINT unique_name_category UNIQUE (name, category)
        );
        """
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        cursor.execute("DROP TABLE IF EXISTS magazines")
        conn.commit()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value,int):
            raise ValueError("ID must be an integer value")
        self._id = value

    @property
    def name(self):
        if self._id is not None:
            sql = "SELECT name FROM magazines WHERE id = ?"
            cursor.execute(sql, (self.id,))
            result = cursor.fetchone()
            if result:
                 return result[0]
        return self._name


    @name.setter
    def name(self, value):
        if not isinstance(value,str):
            raise TypeError("Name must be a string")
        if not 2 <= len(value) <= 16:
            raise ValueError("Names must be between 2 and 16 characters, inclusive")
        self._name = value

    @property
    def category(self):
        if self._id is not None:
            sql = "SELECT category FROM magazines WHERE id = ?"
            cursor.execute(sql, (self.id,))
            result = cursor.fetchone()
            if result:
                return result[0]
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value,str):
            raise TypeError("Category must be a string")
        if len(value) == 0:
            raise ValueError("Category cannot be empty")
        self._category = value

    def save(self):
        sql = "INSERT INTO magazines(name,category)VALUES(?,?)"
        cursor.execute(sql, (self.name, self.category))
        conn.commit()
        self.id = cursor.lastrowid

    @classmethod
    def create(cls, name, category):
        sql = "SELECT id FROM magazines WHERE name = ? AND category = ?"
        cursor.execute(sql, (name, category))
        existing_magazine = cursor.fetchone()
        if existing_magazine:
            raise ValueError("A magazine with the same name and category already exists")
    
        magazine = cls(name, category)
        magazine.save()
        return magazine

        
    def articles(self):
        sql = "SELECT title FROM articles WHERE magazine_id = ?"
        cursor.execute(sql, (self.id,))
        result = cursor.fetchall()
        article_titles = [row[0] for row in result]
        return article_titles

    def contributors(self):
        sql = """
        SELECT DISTINCT authors.name
        FROM articles
        INNER JOIN authors ON articles.author_id = authors.id
        WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self.id,))
        contributor_names = [row[0] for row in cursor.fetchall()]
        return contributor_names

    def article_titles(self):
        sql = "SELECT title FROM articles WHERE magazine_id = ?"
        cursor.execute(sql, (self.id,))
        article_titles = [row[0] for row in cursor.fetchall()]
        return article_titles

    def contributing_authors(self):
        sql = """
            SELECT authors.id, authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(*) > 2
            """
        cursor.execute(sql, (self.id,))
        authors_data = cursor.fetchall()

        # Check if there are any authors with more than 2 publications
        if not authors_data:
            return None

        # Convert data to Author objects
        contributing_authors = []
        for author_id, author_name in authors_data:
            author = Author(name=author_name, id=author_id)
            contributing_authors.append(author)

        return contributing_authors

    def __repr__(self):
        return f'<Magazine {self.name}>'

