from database.connection import get_db_connection

class Article:
    def __init__(self, article_id, title, content, author_id, magazine_id):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._save_to_db()

    def _save_to_db(self):
        connection = get_db_connection()
        with connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO articles (id, title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.article_id, self.title, self.content, self.author_id, self.magazine_id)
            )

    @property
    def get_title(self):
        return self.title

    @property
    def get_content(self):
        return self.content

    @property
    def get_author_id(self):
        return self.author_id

    @property
    def get_magazine_id(self):
        return self.magazine_id

    def __repr__(self):
        return (
            f"Article("
            f"id={self.article_id}, title='{self.title}', content='{self.content}', "
            f"author_id={self.author_id}, magazine_id={self.magazine_id})"
        )