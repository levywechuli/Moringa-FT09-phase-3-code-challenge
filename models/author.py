from database.connection import get_db_connection

class Author:
    def __init__(self, author_id, author_name):
        self.author_id = author_id
        self.author_name = author_name
        self._add_to_database()

    def _add_to_database(self):
        connection = get_db_connection()
        with connection:
            connection.execute(
                "INSERT OR IGNORE INTO authors (id, name) VALUES (?, ?)",
                (self.author_id, self.author_name)
            )

    @property
    def id(self):
        return self.author_id

    @property
    def name(self):
        return self.author_name

    def get_articles(self):
        from models.article import Article  
        connection = get_db_connection()
        with connection:
            result = connection.execute(
                "SELECT * FROM articles WHERE author_id = ?", (self.author_id,)
            ).fetchall()
        return [Article(row[0], row[1], row[2], self, row[4]) for row in result]

    def get_magazines(self):
        from models.magazine import Magazine  
        query = """
            SELECT DISTINCT magazines.* 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id 
            WHERE articles.author_id = ?
        """
        connection = get_db_connection()
        with connection:
            result = connection.execute(query, (self.author_id,)).fetchall()
        return [Magazine(row[0], row[1], row[2]) for row in result]

    def __repr__(self):
        return f"Author(name='{self.author_name}', id={self.author_id})"

