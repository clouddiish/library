class UserNotFoundError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class Book:
    last_id = 0

    @classmethod
    def generate_id(cls):
        cls.last_id += 1
        return cls.last_id

    def __init__(self, title, author):
        self.id = Book.generate_id()
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        self.available = False

    def unborrow(self):
        self.available = True


class User:
    def __init__(self, username, is_admin):
        self.username = username
        self.borrowed_books = []
        self.is_admin = is_admin

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
                print(f"- ID {book.id}: {book.title} by {book.author}")

    def change_admin(self):
        self.is_admin = not self.is_admin


class Library:
    def __init__(self):
        self.users = {}
        self.books = []

    def print_books(self, books):
        for book in books:
            print(
                f"- ID {book.id}: '{book.title}' by {book.author}, available: {book.available}"
            )

    def print_users(self, users):
        for user in users:
            print(
                f"- User: {user}, books borrowed: {len(users[user].borrowed_books)}, admin: {users[user].is_admin}"
            )

    def username_exists(self, user_name):
        if user_name in self.users:
            return True

        return False

    def get_user(self, user_name):
        if self.username_exists(user_name):
            return self.users[user_name]

        raise UserNotFoundError

    def get_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book

        raise BookNotFoundError

    def add_user(self, user_name, is_admin):
        if user_name not in self.users:
            self.users[user_name] = User(user_name, is_admin)
        else:
            print("This username is already taken.")

    def add_book(self, title, author):
        self.books.append(Book(title, author))

    def remove_user(self, user_name):
        try:
            del self.users[user_name]
        except KeyError:
            raise UserNotFoundError

    def remove_book(self, book_id):
        try:
            self.books.remove(self.get_book(book_id))
        except BookNotFoundError:
            raise BookNotFoundError

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
        try:
            book = self.get_book(book_id)
            user = self.get_user(user_name)

            if book in user.borrowed_books:
                book.unborrow()
                user.unborrow(book)
                print("Book returned.")
            else:
                print("You did not borrow this book.")
        except BookNotFoundError:
            print("Book does not exist in the library.")

    def get_available(self):
        return [book for book in self.books if book.available == True]


def library_init(library):
    library.add_book("Abc", "Anne Bee")
    library.add_book("Def", "Cee Dee")
    library.add_book("Ghi", "Eri Foo")

    library.add_user("Gina", True)
    library.add_user("Hannah", False)
    library.add_user("Izzy", False)


def login(library):
    input_username = input("Who are you? ")

    while not library.username_exists(input_username):
        print("This user is not registered at the library.")
        answ = input("Do you want to register? (Y/N) ").lower()

        if answ == "y":
            library.add_user(input_username, False)
            print("User registered.")
            return
        elif answ == "n":
            return
        else:
            print("Please log in again.")

        input_username = input("Who are you? ")

    return input_username


def do_action(action, library, user_name):
    match action:
        case "vb":
            # view all books
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            print("ALL BOOKS:")
            library.print_books(library.books)

        case "vu":
            # view all users
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            print("LIBRARY USERS:")
            library.print_users(library.users)

        case "au":
            # add user
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            new_username = input("New username: ")
            library.add_user(new_username, False)
            print("User added.")

        case "ab":
            # add book
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            new_title = input("New title: ")
            new_author = input("New author: ")
            library.add_book(new_title, new_author)
            print("Book added.")

        case "rmu":
            # remove user
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            del_username = input("Username to remove: ")
            library.remove_user(del_username)
            print("User removed.")

        case "rmb":
            # remove book
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            del_bookid = int(input("Book ID to remove: "))
            library.remove_book(del_bookid)
            print("Book removed.")

        case "cua":
            # change user admin status
            if not library.get_user(user_name).is_admin:
                print("Action not allowed")
                return
            usr_name = input("Username to change admin status: ")

            if usr_name != user_name:
                library.get_user(usr_name).change_admin()
                print("Admin status changed.")
            else:
                print("You cannot change your own admin status.")

        case "vmb":
            # view my borrowed books
            print("MY BORROWED BOOKS:")
            library.get_user(user_name).print_borrowed()

        case "vab":
            # view available books
            print("AVAILABLE BOOKS:")
            library.print_books(library.get_available())

        case "bb":
            # borrow a book
            book_id = int(input("ID of the book you want to borrow: "))
            library.borrow(book_id, user_name)

        case "rb":
            # return a book
            book_id = int(input("ID of the book you want to return: "))
            library.unborrow(book_id, user_name)

        case _:
            print("Wrong option provided")


def action_loop(library, user_name):
    admin_menu = """What do you want to do?
        - vb - view all books
        - vu - view all users
        - au - add user
        - ab - add book
        - rmu - remove user
        - rmb - remove book
        - cua - change user admin status
        - vmb - view my books
        - vab - view available books
        - bb - borrow a book
        - rb - return a book
        - lgo - logout
        """

    user_menu = """What do you want to do?
        - vmb - view my books
        - vab - view available books
        - bb - borrow a book
        - rb - return a book
        - lgo - logout
        """

    while True:
        print()
        if library.get_user(user_name).is_admin:
            action = input(admin_menu).lower()
        else:
            action = input(user_menu).lower()

        if action == "lgo":
            break

        do_action(action, library, user_name)


def run():
    town_lib = Library()
    library_init(town_lib)

    while True:
        print()
        menu_choice = input(
            """Welcome to the library. What do you want to do?
        - l - log in
        - e - exit the library
        """
        ).lower()

        try:
            match menu_choice:
                case "l":
                    logged_user = login(town_lib)
                    if logged_user == None:
                        continue
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
            print("Book does not exist in the library.")
            action_loop(town_lib, logged_user)


run()
