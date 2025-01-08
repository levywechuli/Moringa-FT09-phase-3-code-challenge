from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        if not (2 <= len(name) <= 16) or not isinstance(name, str):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        
        self._id = id
        self._name = name
        self._category = category



    def _create_magazine_in_db(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)",
                       (self._id, self._name, self._category))
        CONN.commit()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not (2 <= len(name) <= 16) or not isinstance(name, str):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def articles(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = CURSOR.fetchall()
        CONN.close()
        return articles

    def contributors(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT DISTINCT authors.* FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        contributors = CURSOR.fetchall()
        CONN.close()
        return contributors

    def article_titles(self):
        articles = self.articles()
        return [article['title'] for article in articles] if articles else None

    def contributing_authors(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        contributing_authors = CURSOR.fetchall()
        CONN.close()
        return contributing_authors if contributing_authors else None