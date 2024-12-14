# Library Management System API Documentation

## Overview

This is the backend API for a Library Management System developed in Python using Django. The system allows librarians (admins) to manage book borrow requests, approve or deny them, and view users' borrow histories. Library users can request books, view available books, and track their borrowing history.

## Technologies

- **Backend:** Python (Django)
- **Database:** SQL (MySQL or PostgreSQL)
- **Authentication:** Basic Authentication (JWT for bonus feature)

## API Endpoints

### 1. Librarian APIs

#### **Create a New Library User**
- **Endpoint:** `POST /api/users/create/`
- **Description:** Create a new library user (for librarian).
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    ```
- **Response:**
    ```json
    {
        "message": "User created successfully"
    }
    ```

#### **View All Book Borrow Requests**
- **Endpoint:** `GET /api/borrow/requests/`
- **Description:** View all pending book borrow requests.
- **Response:**
    ```json
    [
        {
            "user": "user@example.com",
            "book": "Book Title",
            "borrow_start_date": "2024-12-01",
            "borrow_end_date": "2024-12-15",
            "status": "pending"
        }
    ]
    ```

#### **Approve or Deny Borrow Request**
- **Endpoint:** `POST /api/borrow/requests/{request_id}/approve/`
- **Description:** Approve or deny a borrow request.
- **Request Body:**
    ```json
    {
        "status": "approved"
    }
    ```
    (Change `"status": "denied"` to deny the request.)
- **Response:**
    ```json
    {
        "message": "Request approved"
    }
    ```

#### **View a User’s Book Borrow History**
- **Endpoint:** `GET /api/users/{user_id}/borrow-history/`
- **Description:** View a specific user’s book borrow history.
- **Response:**
    ```json
    [
        {
            "book": "Book Title",
            "borrow_start_date": "2024-12-01",
            "borrow_end_date": "2024-12-15",
            "status": "returned"
        }
    ]
    ```

---

### 2. Library User APIs

#### **Get List of Available Books**
- **Endpoint:** `GET /api/books/`
- **Description:** Retrieve the list of available books.
- **Response:**
    ```json
    [
        {
            "id": 1,
            "title": "Book Title",
            "author": "Author Name",
            "isbn": "1234567890",
            "available_copies": 5
        }
    ]
    ```

#### **Submit a Request to Borrow a Book**
- **Endpoint:** `POST /api/borrow/`
- **Description:** Submit a request to borrow a book for a specific time period.
- **Request Body:**
    ```json
    {
        "book_id": 1,
        "borrow_start_date": "2024-12-01",
        "borrow_end_date": "2024-12-15"
    }
    ```
- **Response:**
    ```json
    {
        "message": "Request submitted successfully"
    }
    ```

#### **View Personal Book Borrow History**
- **Endpoint:** `GET /api/users/{user_id}/borrow-history/`
- **Description:** View your own borrowing history.
- **Response:**
    ```json
    [
        {
            "book": "Book Title",
            "borrow_start_date": "2024-12-01",
            "borrow_end_date": "2024-12-15",
            "status": "returned"
        }
    ]
    ```

---

### 3. Edge Case Handling

- **Overlapping Borrow Dates:** If two users try to borrow the same book for overlapping dates, the system will reject the request with a `400 Bad Request` error.

    **Error Response:**
    ```json
    {
        "error": "The book is already borrowed for the requested dates."
    }
    ```

- **Invalid or Incomplete Requests:** If the borrow request is incomplete or contains invalid data, the system will return a `400 Bad Request` error.

    **Error Response:**
    ```json
    {
        "error": "Invalid or incomplete data."
    }
    ```

- **Requests for Non-Existent Users or Books:** If the user or book does not exist, the system will return a `404 Not Found` error.

    **Error Response:**
    ```json
    {
        "error": "User or Book not found."
    }
    ```

---


  
- Use the token in the `Authorization` header for all API requests:


---

### Database Schema Design

1. **Users Table:**
  - `id` (Primary Key)
  - `email` (Unique)
  - `password` (Hashed)
  - `is_librarian` (Boolean)

2. **Books Table:**
  - `id` (Primary Key)
  - `title`
  - `author`
  - `isbn` (Unique)
  - `available_copies`

3. **Borrow Requests Table:**
  - `id` (Primary Key)
  - `user_id` (Foreign Key to Users)
  - `book_id` (Foreign Key to Books)
  - `borrow_start_date`
  - `borrow_end_date`
  - `status` (pending, approved, denied)

4. **Borrow History Table:**
  - `id` (Primary Key)
  - `user_id` (Foreign Key to Users)
  - `book_id` (Foreign Key to Books)
  - `borrow_start_date`
  - `borrow_end_date`
  - `status` (returned, overdue, active)

---

### Testing the API with Postman

1. **Authentication:** Use Basic Authentication for normal users or JWT tokens for bonus features.
2. **Test Scenarios:**
  - **Create User:** Test user creation via `/api/users/create/`.
  - **Borrow Book:** Test book borrowing via `/api/borrow/`.
  - **View Borrow History:** Test viewing borrow history via `/api/users/{user_id}/borrow-history/`.
  - **Approve/Deny Request:** Test managing borrow requests via `/api/borrow/requests/{request_id}/approve/`.

---

## Running the Project Locally

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/library-management-system.git
  cd library-management-system
  ```

2. Install the dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Apply migrations to set up the database:
  ```bash
  python manage.py migrate
  ```

4. Run the development server:
  ```bash
  python manage.py runserver
  ```

Now you can access the API locally at `http://127.0.0.1:8000/`.

---


