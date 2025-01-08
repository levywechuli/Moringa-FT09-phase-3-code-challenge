from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        if not isinstance(content, str):
            raise ValueError("Content must be a string.")
        
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id


    def _create_article_in_db(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("INSERT INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)",
                       (self._id, self._title, self._content, self._author_id, self._magazine_id))
        CONN.commit()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def author(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("SELECT * FROM authors WHERE id = ?", (self._author_id,))
        author = CURSOR.fetchone()
        CONN.close()
        return author

    @property
    def magazine(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("SELECT * FROM magazines WHERE id = ?", (self._magazine_id,))
        magazine = CURSOR.fetchone()
        CONN.close()
        return magazine