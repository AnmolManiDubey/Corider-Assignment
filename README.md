# Corider-Assignment

This is a simple Flask-based REST API for managing users, performing CRUD operations, and storing user data in a MongoDB database.

## Features

- Create a new user (POST /users)
- Retrieve all users (GET /users)
- Retrieve a specific user by ID (GET /users/)
- Update an existing user (PUT /users/)
- Delete a user (DELETE /users/)
- Frontend interface (index.html) for testing operations

## libraries used

- Python 3.8+
- MongoDB
- Flask
- pymongo
- dotenv

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your MongoDB URI:
   ```
   MONGO_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/your_database
   ```
5. Run the application:
   ```sh
   python app.py
   ```
6. Open `http://127.0.0.1:5000/` in your browser to access the frontend.

## API Endpoints

### 1. Get all users

```http
GET /users
```

**Response:**

```json
[
    {
        "_id": "60c72b2f9f1b8c001f9e4c77",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "hashed_password"
    }
]
```

### 2. Get a specific user

```http
GET /users/<id>
```

### 3. Create a new user

```http
POST /users
```

**Request Body:**

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
}
```

### 4. Update a user

```http
PUT /users/<id>
```

**Request Body:**

```json
{
    "name": "Updated Name"
}
```

### 5. Delete a user

```http
DELETE /users/<id>
```

## Error Handling

- `400 Bad Request`: Invalid input or missing required fields.
- `404 Not Found`: User not found.
- `409 Conflict`: User with the same email already exists.

## Testing with Postman

- Use Postman to send GET, POST, PUT, and DELETE requests to the endpoints.


