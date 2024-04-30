from DB import BaseModel, DB, UserModel, BookModel

if __name__ == "__main__":
    db = DB()
    users = UserModel(db.get_connection())
    books = BookModel(db.get_connection())
    users.insert(["admin", "12345678", "1"])
    users.insert(["student", "12345678", "0"])
    books.insert(["Книга Властелин колец 1", "lol", "https://knijky.ru/books/vlastelin-kolec-bratstvo-kolca"])
    books.insert(["Книга Властелин колец 2", "lol", "https://knijky.ru/books/vlastelin-kolec-dve-kreposti"])
    books.insert(["Книга Властелин колец 3", "lol", "https://knijky.ru/books/vlastelin-kolec-vozvrashchenie-korolya"])
    print(users.select())
    print(books.select())
