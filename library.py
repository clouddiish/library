class Book:
    last_id = 0

    def __init__(self, title, author, year):
        self.id = self.last_id + 1
        self.title = title
        self.author = author
        self.year = year
        self.available = True

    def borrow(self):
        self.available = False

    def unborrow(self):
        self.available = True


class User:
    last_id = 0

    def __init__(self, name):
        self.id = self.last_id + 1
        self.name = name
        self.borrowed_books = []

    def borrow(book_title):
        pass

    def unborrow(book_title):
        pass

    def view_available():
        pass


class Library:
    def __init__(self):
        self.users = []
        self.books = []

    def add_user(self, user_name):
        self.users.append(User(user_name))

    def add_book(self, title, author, year):
        self.books.append(Book(title, author, year))

    def remove_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                self.users.remove(user)

    def remove_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.users.remove(book)
