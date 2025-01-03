import pytest
from library import Book, User, Library, UserNotFoundError, BookNotFoundError


# arrange
@pytest.fixture
def clear_last_id():
    Book.last_id = 0


def test_add_user():
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
    # arrange
    Book.last_id = 0
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


def test_get_book(clear_last_id):
    # arrange
    Book.last_id = 0
    lib = Library()
    lib.add_book("Test title", "Test author")

    # act
    found_book = lib.get_book(1)

    # assert
    assert found_book.id == 1


def test_remove_user():
    # arrange
    lib = Library()
    lib.add_user("Test user", False)

    # act
    lib.remove_user("Test user")

    # assert
    assert len(lib.users) == 0, "User was not removed"


def test_remove_nonexistent_user():
    # arrange
    lib = Library()

    # act, assert
    with pytest.raises(UserNotFoundError):
        lib.remove_user("Test user")


def test_remove_book(clear_last_id):
    # arrange
    lib = Library()
    lib.add_book("Test title", "Test author")

    # act
    lib.remove_book(1)

    # assert
    assert len(lib.books) == 0, "Book was not removed"


def test_remove_nonexistent_book(clear_last_id):
    # arrange
    lib = Library()

    # act, assert
    with pytest.raises(BookNotFoundError):
        lib.remove_book(5)


def test_borrow(clear_last_id):
    # arrange
    lib = Library()
    lib.add_user("Test user", False)
    lib.add_book("Test title", "Test author")

    # act
    lib.borrow(1, "Test user")

    # assert
    assert (
        len(lib.users["Test user"].borrowed_books) == 1
    ), "Book was not added to borrowed books of the user"
    assert (
        lib.books[0].available == False
    ), "Book availability status was not changed to False"


def test_borrow_unavailable_book(clear_last_id):
    # arrange
    lib = Library()
    lib.add_user("Test user", False)
    lib.add_user("Test user 2", False)
    lib.add_book("Test title", "Test author")

    # act
    lib.borrow(1, "Test user")
    lib.borrow(1, "Test user 2")

    # assert
    assert (
        len(lib.users["Test user 2"].borrowed_books) == 0
    ), "Book was added to borrowed books of the user"
    assert lib.books[0].available == False, "Book availability status is not False"


def test_borrow_nonexistent_book(clear_last_id):
    # arrange
    lib = Library()
    lib.add_user("Test user", False)

    # act, assert
    with pytest.raises(BookNotFoundError):
        lib.borrow(1, "Test user")
