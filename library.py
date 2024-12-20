class UserNotFoundError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class Book:
    last_id = 0

    def __init__(self, title, author):
        self.id = self.last_id + 1
        Book.last_id = self.last_id + 1
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        self.available = False

    def unborrow(self):
        self.available = True


class User:
    def __init__(self, username):
        self.username = username
        self.borrowed_books = []

    def borrow(self, book):
        self.borrowed_books.append(book)

    def unborrow(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def print_borrowed(self):
        if len(self.borrowed_books) == 0:
            print("No books borrowed.")
        else:
            for book in self.borrowed_books:
                print("Borrowed books:")
                print(f"- ID {book.id}: {book.title} by {book.author}")


class Library:
    def __init__(self):
        self.users = []
        self.books = []

    def print_books(self, books):
        for book in books:
            print(
                f"- ID {book.id}: '{book.title}' by {book.author}, available: {book.available}"
            )

    def print_users(self, users):
        for user in users:
            print(
                f"- User: {user.username}, books borrowed: {len(user.borrowed_books)}"
            )

    def username_exists(self, user_name):
        for user in self.users:
            if user_name == user.username:
                return True

        return False

    def get_user(self, user_name):
        for user in self.users:
            if user.username == user_name:
                return user

        raise UserNotFoundError

    def get_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book

        raise BookNotFoundError

    def add_user(self, user_name):
        self.users.append(User(user_name))

    def add_book(self, title, author):
        self.books.append(Book(title, author))

    def remove_user(self, user_name):
        self.users.remove(self.get_user(user_name))

    def remove_book(self, book_id):
        self.books.remove(self.get_book(book_id))

    def borrow(self, book_id, user_name):
        book = self.get_book(book_id)
        user = self.get_user(user_name)

        if book.available:
            book.borrow()
            user.borrow(book)
            print("Book borrowed.")
        else:
            print("Book not available.")

    def unborrow(self, book_id, user_name):
        book = self.get_book(book_id)
        user = self.get_user(user_name)

        if book in user.borrowed_books:
            book.unborrow()
            user.unborrow(book)
            print("Book returned.")
        else:
            print("You did not borrow this book.")

    def get_available(self):
        return [book for book in self.books if book.available == True]


def library_init(library):
    library.add_book("Abc", "Anne Bee")
    library.add_book("Def", "Cee Dee")
    library.add_book("Ghi", "Eri Foo")

    library.add_user("Gina")
    library.add_user("Hannah")
    library.add_user("Izzy")


def login(library):
    input_username = input("Who are you? ")

    while not library.username_exists(input_username):
        print("This user is not registered at the library.")
        answ = input("Do you want to register? (Y/N) ").lower()

        if answ == "y":
            library.add_user(input_username)
            print("User registered. Please log in again.")
        else:
            print("Please log in again.")

        input_username = input("Who are you? ")

    return input_username


def do_action(action, library, user_name):
    match action:
        case "vb":
            library.print_books(library.books)

        case "vu":
            library.print_users(library.users)

        case "vmb":
            library.get_user(user_name).print_borrowed()

        case "vab":
            library.print_books(library.get_available())

        case "bb":
            book_id = int(input("ID of the book you want to borrow: "))
            library.borrow(book_id, user_name)

        case "rb":
            book_id = int(input("ID of the book you want to return: "))
            library.unborrow(book_id, user_name)

        case _:
            print("Wrong option provided")


def action_loop(library, user_name):
    action = input(
        """
                    What do you want to do?
                    - vb - view all books
                    - vu - view all users
                    - vmb - view my books
                    - vab - view available books
                    - bb - borrow a book
                    - rb - return a book
                    - lgo - logout
                    """
    ).lower()

    while action != "lgo":
        do_action(action, library, user_name)

        action = input(
            """
                What do you want to do?
                - vb - view all books
                - vu - view all users
                - vmb - view my books
                - vab - view available books
                - bb - borrow a book
                - rb - return a book
                - lgo - logout
                """
        ).lower()


def run():
    town_lib = Library()
    library_init(town_lib)

    while True:
        menu_choice = input(
            """
            Welcome to the library. What do you want to do?
            - l - log in
            - e - exit the library
            """
        ).lower()

        try:
            match menu_choice:
                case "l":
                    logged_user = login(town_lib)
                    action_loop(town_lib, logged_user)
                case "e":
                    sure = input("Are you sure? (Y/N) ").lower()
                    if sure == "y":
                        break
                case _:
                    print("Wrong letter provided.")
        except UserNotFoundError:
            print("User not found.")
            action_loop(town_lib, logged_user)
        except BookNotFoundError:
            print("Book not found.")
            action_loop(town_lib, logged_user)


run()
