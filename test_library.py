import pytest
from library import Book, User, Library, UserNotFoundError, BookNotFoundError


# arrange
@pytest.fixture
def clear_last_id():
    Book.last_id = 0


@pytest.fixture
def initialise_library(clear_last_id):
    lib = Library()

    lib.add_user("Test user", False)
    lib.add_user("Test user 2", False)

    lib.add_book("Test title", "Test author")

    return lib


def test_add_user_when_user_is_unique():
    """
    Test that user with unique username is added to the library
    """
    # arrange
    lib = Library()
    user_name = "Test user"
    is_admin = False

    # act
    lib.add_user(user_name, is_admin)

    # assert
    assert len(lib.users) == 1, "User was not added to the library"
    added_user = lib.users[user_name]
    assert added_user.username == user_name, "The username is incorrect"
    assert added_user.is_admin == is_admin, "The admin status of the user is incorrect"


def test_add_book():
    """
    Test that book is added to the library
    """
    # arrange
    lib = Library()
    title = "Test Title"
    author = "Test author"

    # act
    lib.add_book(title, author)

    # assert
    assert len(lib.books) == 1, "Book was not added to the library"
    added_book = lib.books[0]
    assert added_book.title == title, "Book's title is incorrect"
    assert added_book.author == author, "Book's author is incorrect"
    assert added_book.available == True, "Book's availability should be True by default"
    assert Book.last_id == 1, "Book last_id property is not 1"


def test_get_book_when_book_exists(initialise_library):
    """
    Check if it's possible to get a book that exists in the library
    """

    # arrange
    lib = initialise_library

    # act
    found_book = lib.get_book(1)

    # assert
    assert found_book.id == 1


def test_get_book_when_book_is_nonexistent(initialise_library):
    """
    Test that a BookNotFoundError is raised when trying to get a nonexistent book
    """

    # arrange
    lib = initialise_library

    # act, assert
    with pytest.raises(BookNotFoundError):
        found_book = lib.get_book(10)


def test_remove_user_when_user_exist(initialise_library):
    """
    Test that an existing user is removed
    """

    # arrange
    lib = initialise_library
    initial_no_users = len(lib.users)

    # act
    lib.remove_user("Test user")
    new_no_users = len(lib.users)

    # assert
    assert initial_no_users - new_no_users == 1, "User was not removed"


def test_remove_user_when_user_is_nonexistent():
    """
    Test that a UserNotFoundError is raised when trying to remove a nonexistent user
    """

    # arrange
    lib = Library()

    # act, assert
    with pytest.raises(UserNotFoundError):
        lib.remove_user("Test user")


def test_remove_book_when_book_exists(initialise_library):
    """
    Test that an existing book is removed from the library
    """

    # arrange
    lib = initialise_library

    # act
    lib.remove_book(1)

    # assert
    assert len(lib.books) == 0, "Book was not removed"


def test_remove_book_when_book_is_nonexistent(initialise_library):
    """
    Test that a BookNotFoundError is raised when trying to remove a nonexistent book
    """

    # arrange
    lib = initialise_library

    # act, assert
    with pytest.raises(BookNotFoundError):
        lib.remove_book(10)


def test_borrow_when_book_is_available(initialise_library):
    """
    Test that an available existent book is borrowed by an existing user
    """

    # arrange
    lib = initialise_library

    # act
    lib.borrow(1, "Test user")

    # assert
    assert (
        len(lib.users["Test user"].borrowed_books) == 1
    ), "Book was not added to borrowed books of the user"
    assert (
        lib.books[0].available == False
    ), "Book availability status was not changed to False"


def test_borrow_book_when_book_is_unavailable(capsys, initialise_library):
    """
    Test that an existing book is not borrowed when it's unavailable
    and if an appropriate message is printed to the user
    """

    # arrange
    lib = initialise_library
    attempted_user = lib.get_user("Test user 2")

    # act
    lib.borrow(1, "Test user")
    lib.borrow(1, attempted_user.username)

    captured = capsys.readouterr().out.split("\n")
    message = captured[-2]

    # assert
    assert message == "Book not available.", "Message was not printed to the user"
    assert lib.get_book(1).available == False, "Book availability status is not False"
    assert len(attempted_user.borrowed_books) == 0, "User borrowed an unavailable book"


def test_borrow_book_when_book_is_nonexistent(initialise_library):
    """
    Test that a BookNotFoundError is raised when user tries to borrow a nonexistent book
    """

    # arrange
    lib = initialise_library

    # act, assert
    with pytest.raises(BookNotFoundError):
        lib.borrow(10, "Test user")


def test_unborrow_when_book_is_borrowed_by_the_user(initialise_library):
    """
    Test that a borrowed book is unborrowed
    """

    # arrange
    lib = initialise_library

    # act
    lib.borrow(1, "Test user")
    lib.unborrow(1, "Test user")

    # assert
    assert (
        len(lib.users["Test user"].borrowed_books) == 0
    ), "Book was not removed from borrowed books of the user"
    assert (
        lib.books[0].available == True
    ), "Book availability status was not changed to True"


def test_unborrow_when_book_is_not_borrowed_by_anyone(capsys, initialise_library):
    """
    Test that an unborrowed book is not unborrowed when user tries to unborrow it,
    and if an appropriate message is printed to the user
    """

    # arrange
    lib = initialise_library
    attempted_book = lib.get_book(1)
    attempted_user = lib.get_user("Test user")

    # act
    lib.unborrow(1, attempted_user.username)

    captured = capsys.readouterr().out.split("\n")
    message = captured[-2]

    # assert
    assert (
        message == "You did not borrow this book."
    ), "Message was not printed to the user"
    assert attempted_book.available == True, "Book availability status is not True"
    assert (
        len(attempted_user.borrowed_books) == 0
    ), "User's borrowed books are not empty"


def test_unborrow_book_when_book_is_nonexistent(capsys, initialise_library):
    """
    Test that a nonexistent book is not borrowed,
    and if an appropriate message is printed to the user
    """

    # arrange
    lib = initialise_library
    attempted_user = lib.get_user("Test user")

    # act
    lib.unborrow(10, attempted_user.username)
    captured = capsys.readouterr().out.split("\n")
    message = captured[-2]

    # assert
    assert (
        message == "Book does not exist in the library."
    ), "Message was not printed to the user"
    assert (
        len(attempted_user.borrowed_books) == 0
    ), "User's borrowed books are not empty"
