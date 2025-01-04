class UserNotFoundError(Exception):
    """
    Exception raised when a user is not found in the library.
    """

    pass


class BookNotFoundError(Exception):
    """
    Exception raised when a book is not found in the library.
    """

    pass


class Book:
    """
    A class to represent a book in the library.

    Attributes:
        last_id (int): The last assigned ID for books.
        id (int): Unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        available (bool): The availability status of the book.
    """

    last_id = 0

    @classmethod
    def generate_id(cls):
        """
        Generates a unique ID for a book.

        Returns:
            int: The generated unique ID.
        """
        cls.last_id += 1
        return cls.last_id

    def __init__(self, title, author):
        """
        Initializes a new Book instance.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
        """
        self.id = Book.generate_id()
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        """
        Marks the book as borrowed (unavailable).
        """
        self.available = False

    def unborrow(self):
        """
        Marks the book as available.
        """
        self.available = True


class User:
    """
    A class to represent a library user.

    Attributes:
        username (str): The username of the user.
        borrowed_books (list): A list of books borrowed by the user.
        is_admin (bool): Indicates if the user is an admin.
    """

    def __init__(self, username, is_admin):
        """
        Initializes a new User instance.

        Args:
            username (str): The username of the user.
            is_admin (bool): The admin status of the user.
        """
        self.username = username
        self.borrowed_books = []
        self.is_admin = is_admin

    def borrow(self, book):
        """
        Adds a book to the user's borrowed list.

        Args:
            book (Book): The book to borrow.
        """
        self.borrowed_books.append(book)

    def unborrow(self, book):
        """
        Removes a book from the user's borrowed list.

        Args:
            book (Book): The book to return.
        """
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def print_borrowed(self):
        """
        Prints the list of borrowed books.
        """
        if len(self.borrowed_books) == 0:
            print("No books borrowed.")
        else:
            for book in self.borrowed_books:
                print(f"- ID {book.id}: {book.title} by {book.author}")

    def change_admin(self):
        """
        Toggles the admin status of the user.
        """
        self.is_admin = not self.is_admin


class Library:
    """
    A class to represent a library.

    Attributes:
        users (dict): A dictionary of library users, keyed by username.
        books (list): A list of books in the library.
    """

    def __init__(self):
        """
        Initializes a new Library instance.
        """
        self.users = {}
        self.books = []

    def print_books(self, books):
        """
        Prints details of books in the library.

        Args:
            books (list): A list of books to print.
        """
        for book in books:
            print(
                f"- ID {book.id}: '{book.title}' by {book.author}, available: {book.available}"
            )

    def print_users(self, users):
        """
        Prints details of users in the library.

        Args:
            users (dict): A dictionary of users to print.
        """
        for user in users:
            print(
                f"- User: {user}, books borrowed: {len(users[user].borrowed_books)}, admin: {users[user].is_admin}"
            )

    def username_exists(self, user_name):
        """
        Checks if a username exists in the library.

        Args:
            user_name (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        return user_name in self.users

    def get_user(self, user_name):
        """
        Retrieves a user by username.

        Args:
            user_name (str): The username of the user.

        Returns:
            User: The user with the given username.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        if self.username_exists(user_name):
            return self.users[user_name]
        raise UserNotFoundError

    def get_book(self, book_id):
        """
        Retrieves a book by its ID.

        Args:
            book_id (int): The ID of the book.

        Returns:
            Book: The book with the given ID.

        Raises:
            BookNotFoundError: If the book is not found.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        raise BookNotFoundError

    def add_user(self, user_name, is_admin):
        """
        Adds a new user to the library, if the username is unique.

        Args:
            user_name (str): The username of the new user.
            is_admin (bool): Admin status of the new user.
        """
        if user_name not in self.users:
            self.users[user_name] = User(user_name, is_admin)
            print("User added.")
        else:
            print("This username is already taken.")

    def add_book(self, title, author):
        """
        Adds a new book to the library.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
        """
        self.books.append(Book(title, author))

    def remove_user(self, user_name):
        """
        Removes a user from the library.

        Args:
            user_name (str): The username of the user to remove.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        try:
            del self.users[user_name]
        except KeyError:
            raise UserNotFoundError

    def remove_book(self, book_id):
        """
        Removes a book from the library.

        Args:
            book_id (int): The ID of the book to remove.

        Raises:
            BookNotFoundError: If the book is not found.
        """
        try:
            book_to_remove = self.get_book(book_id)
            self.books.remove(book_to_remove)
        except BookNotFoundError:
            raise BookNotFoundError

    def borrow(self, book_id, user_name):
        """
        Borrows a book for a user if the book is available.

        Args:
            book_id (int): The ID of the book to borrow.
            user_name (str): The username of the user borrowing the book.
        """
        book = self.get_book(book_id)
        user = self.get_user(user_name)

        if book.available:
            book.borrow()
            user.borrow(book)
            print("Book borrowed.")
        else:
            print("Book not available.")

    def unborrow(self, book_id, user_name):
        """
        Returns a borrowed book if the user borrowed it.

        Args:
            book_id (int): The ID of the book to return.
            user_name (str): The username of the user returning the book.
        """
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
        """
        Retrieves all available books in the library.

        Returns:
            list: A list of available books.
        """
        return [book for book in self.books if book.available]


def library_init(library):
    """
    Initializes the library with a predefined set of books and users.

    Args:
        library (Library): The library to initialize.
    """
    library.add_book("Abc", "Anne Bee")
    library.add_book("Def", "Cee Dee")
    library.add_book("Ghi", "Eri Foo")

    library.add_user("Gina", True)
    library.add_user("Hannah", False)
    library.add_user("Izzy", False)


def login(library):
    """
    Logs a user into the library system, with an option to register new users.

    Args:
        library (Library): The library instance.

    Returns:
        str: The username of the logged-in user, or None if login was unsuccessful.
    """
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
    """
    Performs a specific action based on user input.

    Args:
        action (str): The action to perform.
        library (Library): The library instance.
        user_name (str): The username of the user performing the action.
    """
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
            if del_username == user_name:
                print("You cannot remove yourself.")
                return
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
    """
    Handles a continuous loop of actions for a logged-in user.

    Args:
        library (Library): The library instance.
        user_name (str): The username of the logged-in user.
    """
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
    """
    Main function to run the library system.
    """
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
