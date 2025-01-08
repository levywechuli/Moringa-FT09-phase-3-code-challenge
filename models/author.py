from database.connection import get_db_connection

class Author:
    def __init__(self, id, name, email):
        if not name:
            raise ValueError("Name shouldn't be empty.")
        if "@" not in email:
            raise ValueError("Wrong email format.")
        
        self._id = id  
        self._name = name
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    def get_contact_info(self):
        return f"{self.name} <{self.email}>"

    def articles(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = CURSOR.fetchall()
        CONN.close()
        return articles

    def magazines(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        magazines = CURSOR.fetchall()
        CONN.close()
        return magazines

