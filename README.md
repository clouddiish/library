# library management system

Library management system enables library administrators and users to manage and borrow books. The system supports user management, book management, and basic borrowing/returning operations. It provides separate user and admin interfaces for to differentiate between allowed operations. The system includes unit tests for core functionalities.

## features

- **book management** - add, remove and view books in the library
- **user management** - add, remove, view and change admin status
- **user capabilities** - users can borrow and return books, view their borrowed books and view all available books in the library
- **admin capabilities** - admins additionally can view all users, books, and perform privileged actions like adding/removing users or books
- **error handling** - custom exceptions implemented for when invalid book (`BookNotFoundError`) or user (`UserNotFoundError`) are accessed

## getting started

### dependencies

- Python 3.x
- `pytest` for running the tests
```
pip install pytest
```

### installation

- clone the repository or download the code files

```
git clone https://github.com/clouddiish/library.git
```

### run

- run the script with the below command. Note: if needed replace `library.py` with the name of the script

```
python library.py
```

### output

- on running the program, you'll be presented with a menu:
  - l to log in or register
  - e to exit the program

- after logging in:
  - admin users have access to both user and book management menus
  - regular users can only borrow/return books and view available/borrowed books

### run tests

- run the tests with the below command
```
pytest
```

## notes

- as there is no database, the data will not persists between runs of the script
