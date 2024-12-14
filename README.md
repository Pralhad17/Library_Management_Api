**API Documentation for Library Management System**
Overview:
The Library Management System API allows the management of books and users within a library. Librarians (admins) can manage book borrow requests, approve or deny them, and view users’ borrow histories. Users can browse available books, submit requests to borrow books, and view their borrowing history. This documentation outlines the available API endpoints and describes how to use them effectively.

Technologies:
Backend: Python (Django)
Database: SQLite
Authentication: Basic Authentication (with an option for JWT for bonus feature)
1. Librarian APIs:
Create a New Library User
Endpoint: POST /api/users/create/
Description: Allows a librarian to create a new library user.
Request Body:
json
Copy code
{
  "email": "user@example.com",
  "password": "securepassword123"
}
Response:
json
Copy code
{
  "message": "User created successfully"
}
Authentication: Basic Authentication
View All Book Borrow Requests
Endpoint: GET /api/borrow/requests/
Description: Allows a librarian to view all pending book borrow requests.
Response:
json
Copy code
[
  {
    "user": "user@example.com",
    "book": "Book Title",
    "borrow_start_date": "2024-12-01",
    "borrow_end_date": "2024-12-15",
    "status": "pending"
  },
  {
    "user": "user2@example.com",
    "book": "Another Book",
    "borrow_start_date": "2024-12-10",
    "borrow_end_date": "2024-12-20",
    "status": "approved"
  }
]
Authentication: Basic Authentication
Approve or Deny Borrow Request
Endpoint: POST /api/borrow/requests/{request_id}/approve/

Description: Allows the librarian to approve a borrow request.

Request Body:

json
Copy code
{
  "status": "approved"
}
To deny the request, change "status": "denied".

Response:

json
Copy code
{
  "message": "Request approved"
}
Authentication: Basic Authentication

View a User’s Book Borrow History
Endpoint: GET /api/users/{user_id}/borrow-history/
Description: Allows the librarian to view the borrowing history of a specific user.
Response:
json
Copy code
[
  {
    "book": "Book Title",
    "borrow_start_date": "2024-12-01",
    "borrow_end_date": "2024-12-15",
    "status": "returned"
  },
  {
    "book": "Another Book",
    "borrow_start_date": "2024-12-20",
    "borrow_end_date": "2025-01-10",
    "status": "overdue"
  }
]
Authentication: Basic Authentication
2. Library User APIs:
Get List of Available Books
Endpoint: GET /api/books/
Description: Allows a library user to get the list of available books.
Response:
json
Copy code
[
  {
    "id": 1,
    "title": "Book Title",
    "author": "Author Name",
    "isbn": "1234567890",
    "available_copies": 5
  },
  {
    "id": 2,
    "title": "Another Book",
    "author": "Another Author",
    "isbn": "0987654321",
    "available_copies": 3
  }
]
Authentication: Basic Authentication
Submit a Request to Borrow a Book
Endpoint: POST /api/borrow/
Description: Allows a library user to submit a request to borrow a book for specific dates.
Request Body:
json
Copy code
{
  "book_id": 1,
  "borrow_start_date": "2024-12-01",
  "borrow_end_date": "2024-12-15"
}
Response:
json
Copy code
{
  "message": "Request submitted successfully"
}
Authentication: Basic Authentication
View Personal Book Borrow History
Endpoint: GET /api/users/{user_id}/borrow-history/
Description: Allows a user to view their personal borrow history.
Response:
json
Copy code
[
  {
    "book": "Book Title",
    "borrow_start_date": "2024-12-01",
    "borrow_end_date": "2024-12-15",
    "status": "returned"
  },
  {
    "book": "Another Book",
    "borrow_start_date": "2024-12-10",
    "borrow_end_date": "2024-12-20",
    "status": "overdue"
  }
]
Authentication: Basic Authentication
3. Edge Case Handling:
Overlapping Borrow Dates
If two users try to borrow the same book for overlapping dates, the system will reject the request with a 400 Bad Request error.

Error Response:

json
Copy code
{
  "error": "The book is already borrowed for the requested dates."
}
Invalid or Incomplete Requests
If a borrow request is incomplete or contains invalid data (such as missing dates or book ID), the system will return a 400 Bad Request error.

Error Response:

json
Copy code
{
  "error": "Invalid or incomplete data."
}
Requests for Non-Existent Users or Books
If the user or book does not exist in the database, the system will return a 404 Not Found error.

Error Response:

json
Copy code
{
  "error": "User or Book not found."
}

**Users Table:
**
id (Primary Key)
email (Unique)
password (Hashed)
is_librarian (Boolean)
Books Table:

id (Primary Key)
title
author
isbn (Unique)
available_copies
Borrow Requests Table:

id (Primary Key)
user_id (Foreign Key to Users)
book_id (Foreign Key to Books)
borrow_start_date
borrow_end_date
status (pending, approved, denied)
Borrow History Table:

id (Primary Key)
user_id (Foreign Key to Users)
book_id (Foreign Key to Books)
borrow_start_date
borrow_end_date
status (returned, overdue, active)
Testing the API with Postman:
Authentication: Use Basic Authentication for normal users or JWT tokens for bonus.
Testing Scenarios:
Create user (librarian) – Test creating a new user by sending a POST request to /api/users/create/.
Borrow Book – Test borrowing a book using /api/borrow/.
View Borrow History – Check the borrow history using /api/users/{user_id}/borrow-history/.
Approve/Deny Request – Test managing borrow requests via /api/borrow/requests/{request_id}/approve/.
