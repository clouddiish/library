import pytest
from library import Book, User, Library


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


def test_remove_user():
    # arrange
    lib = Library()
    lib.add_user("Test user", False)

    # act
    lib.remove_user("Test user")

    # assert
    assert len(lib.users) == 0, "User was not removed"
