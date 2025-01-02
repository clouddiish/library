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
