# Library Management System API Documentation

## Overview
This API provides endpoints for managing a library system. It allows users to register, log in, and interact with books in the library, including requesting, granting, and returning books. The API uses Flask with SQLAlchemy for data management and JWT for user authentication.

## Authentication
- **JWT Token**: To access some endpoints, users must authenticate using a JSON Web Token (JWT). This token is obtained by logging in and must be provided in the request headers for endpoints requiring authentication.

## Endpoints

---

### User Management

#### Register a New User
- **Endpoint**: `/register`
- **Method**: `POST`
- **Request Parameters**: 
  - `email`: User's email address
  - `password`: User's password
  - `username`: User's name
  - `role`: User's role ID (1 for Staff, 2 for Student)
- **Responses**:
  - `201`: User registered successfully
  - `409`: User already exists
  - `400`: Invalid input

#### User Login
- **Endpoint**: `/login`
- **Method**: `POST`
- **Request Parameters**:
  - `email`: User's email address
  - `password`: User's password
- **Responses**:
  - `200`: Successful login with a JWT token in the response
  - `403`: Incorrect password
  - `404`: User not found

---

### Book Management

#### Get All Books
- **Endpoint**: `/getAllBooks`
- **Method**: `GET`
- **Responses**:
  - `200`: Returns a list of all books with their categories and status
  - `404`: No books found

#### Get Available Books
- **Endpoint**: `/getAvailableBooks`
- **Method**: `GET`
- **Responses**:
  - `200`: Returns a list of available books with their categories
  - `404`: No available books found

#### Get Current Owner of a Book
- **Endpoint**: `/getCurrentOwner/<int:bookid>`
- **Method**: `GET`
- **Authorization**: Requires JWT (only library staff can check book ownership)
- **Parameters**: 
  - `bookid`: The ID of the book to check
- **Responses**:
  - `200`: Returns information about the current owner or status of the book
  - `404`: Invalid book ID or other error
  - `403`: Unauthorized (if not staff)

---

### Book Requests

#### Request a Book
- **Endpoint**: `/requestABook`
- **Method**: `PUT`
- **Request Parameters**:
  - `bookid`: ID of the book to request (provided as a query parameter)
- **Authorization**: Requires JWT (only students can request books)
- **Responses**:
  - `200`: Book request created
  - `403`: Unauthorized (if not a student)
  - `404`: Book not available or invalid

#### Get Requested Book Status
- **Endpoint**: `/getRequestedBookStatus`
- **Method**: `GET`
- **Authorization**: Requires JWT (only students can view their requests)
- **Responses**:
  - `200`: Returns the status of the requested books
  - `404`: No book requests found
  - `403`: Unauthorized (if not a student)

#### Show All Book Requests
- **Endpoint**: `/showAllBookRequests`
- **Method**: `GET`
- **Authorization**: Requires JWT (only library staff can view all requests)
- **Responses**:
  - `200`: Returns a list of all book requests with user details
  - `404`: No book requests found
  - `403`: Unauthorized (if not staff)

---

### Book Management for Staff

#### Grant a Book
- **Endpoint**: `/grantABook`
- **Method**: `PUT`
- **Request Parameters**:
  - `reqID`: Request ID for the book to grant (provided as a query parameter)
- **Authorization**: Requires JWT (only staff can grant books)
- **Responses**:
  - `200`: Book granted successfully
  - `404`: Request invalid or already approved
  - `403`: Unauthorized (if not staff)

#### Reject a Book
- **Endpoint**: `/rejectABook`
- **Method**: `PUT`
- **Request Parameters**:
  - `reqID`: Request ID for the book to reject (provided as a query parameter)
- **Authorization**: Requires JWT (only staff can reject books)
- **Responses**:
  - `200`: Book request rejected
  - `404`: Request invalid or already approved
  - `403`: Unauthorized (if not staff)

#### Show All Assigned Books
- **Endpoint**: `/showAllAssignedBooks`
- **Method**: `GET`
- **Authorization**: Requires JWT (only staff can view assigned books)
- **Responses**:
  - `200`: Returns a list of all assigned books with borrower details
  - `404`: No books assigned
  - `403`: Unauthorized (if not staff)

#### Return a Book
- **Endpoint**: `/returnABook`
- **Method**: `PUT`
- **Request Parameters**:
  - `reqID`: Request ID for the book to return (provided as a query parameter)
- **Authorization**: Requires JWT (only staff can manage book returns)
- **Responses**:
  - `200`: Book returned successfully
  - `404`: Invalid request ID
  - `403`: Unauthorized (if not staff)

---

### Error Handling
In case of errors, the API returns appropriate HTTP status codes with a corresponding error message. Here are some common HTTP status codes and their meanings:

- **200**: Success
- **201**: Resource created successfully
- **403**: Forbidden (unauthorized access)
- **404**: Resource not found
- **409**: Conflict (duplicate resource)

---

This API documentation provides an overview of the various endpoints and their expected behavior. If further information or clarification is needed, additional details can be added to this document.
