#  Notes API

A secure RESTful Notes API built with **FastAPI**, **SQLAlchemy 2.0**, and **SQLite**. The API supports JWT authentication, user-specific notes, pinning, archiving, soft delete, searching, sorting, and follows RESTful design principles.

---

## Features

### Authentication

- User registration
- User login
- JWT authentication
- Password hashing using **pwdlib**
- Protected endpoints
- Retrieve current authenticated user (`/users/me`)

### Notes Management

- Create notes
- Retrieve all active notes
- Retrieve a note by ID
- Update notes
- Permanently delete notes
- Soft delete notes
- Restore deleted notes
- Pin and unpin notes
- Archive and unarchive notes
- View archived notes
- View deleted notes (Trash)

### Search & Sorting

- Search by title
- Search by content
- Sort by:
  - Title
  - Created date
- Pinned notes always appear first
- Latest updated notes are shown first by default

### Other Features

- User-specific note ownership
- Request & response validation using Pydantic
- SQLAlchemy 2.0 ORM
- Proper HTTP status codes
- Interactive Swagger UI

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Pydantic v2
- PyJWT
- Pwdlib
- Python-dotenv
- Uvicorn

---

## Project Structure

```text
notes-api/
├── assets/
│   └── swagger.png
├── routes/
│   ├── auth.py
│   └── notes.py
├── utils/
│   ├── jwt_handler.py
│   └── security.py
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/qw3rty-dev/fastapi-notes-api.git
```

Navigate to the project directory:

```bash
cd fastapi-notes-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your_secret_key_here
```

Run the server:

```bash
uvicorn main:app --reload
```

---

## Authentication

Most endpoints require authentication.

1. Register a new account.
2. Login using your email and password.
3. Open Swagger UI.
4. Click **Authorize**.
5. Enter:
   - **Username:** your email
   - **Password:** your password
6. Leave Client ID and Client Secret empty.
7. Click **Authorize**.

Swagger automatically includes the JWT in protected requests.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /users/register | Register a new user |
| POST | /users/login | Login and receive JWT |
| GET | /users/me | Retrieve current user |

---

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /notes | Create note |
| GET | /notes | Retrieve active notes |
| GET | /notes/{note_id} | Retrieve note by ID |
| PATCH | /notes/{note_id} | Update note |
| GET | /notes/archived | Retrieve archived notes |
| GET | /notes/trash | Retrieve deleted notes |
| DELETE | /notes/{note_id} | Permanently delete note |

---

## Search & Sorting

Examples:

```http
GET /notes?search=fastapi

GET /notes?sort=title

GET /notes?sort=created_at