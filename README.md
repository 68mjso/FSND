# Movie and Actor API

This API provides CRUD operations for managing movies and actors in a database. The API is secured with role-based permissions and uses Auth0 for authentication. All responses are in JSON format.

## Live Testing: https://hidden-badlands-12697-2a16946ff7b9.herokuapp.com/

## Prerequisites

- **Python 3.7+**
- **Flask** - for API server
- **SQLAlchemy** - for ORM
- **Flask-CORS** - for handling Cross-Origin Resource Sharing
- **Auth0** - for authentication

## Environtment

```bash
    - DB_HOST: <your_database_hosted_server>
    - DB_PORT: <your_database_connection_port>
    - DB_USER: <your_database_username>
    - DB_PASS: <your_database_password>
    - DB_NAME: <your_database_name>
    - AUTH0_DOMAIN: <your_auth0_domain>
    - API_AUDIENCE: <your_auth0_api_audience>
    - API_KEY_1: <api_key_for_testing_casting_assitant>
    - API_KEY_2: <api_key_for_testing_casting_director>
    - API_KEY_3: <api_key_for_testing_executive_producer>
```
## Setup and Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your database and ensure you have models for `Movie` and `Actor` as defined in the `models.py` file.

## Authentication

This API uses Auth0 for authentication and authorization. Each route requires a specific permission.

- **view:movies** - for viewing movie data.
- **post:movies** - for adding a new movie.
- **patch:movies** - for updating an existing movie.
- **delete:movies** - for deleting a movie.
- **view:actors** - for viewing actor data.
- **post:actors** - for adding a new actor.
- **patch:actors** - for updating an existing actor.
- **delete:actors** - for deleting an actor.

## Endpoints

### Movies

#### GET /movies

- **Description**: Fetch all movies.
- **Permissions**: `view:movies`
- **Response**:
  - `status`: 200
  - `data`: List of movies, each with `id`, `title`, and `release_date`.

#### POST /movies

- **Description**: Add a new movie.
- **Permissions**: `post:movies`
- **Request Body**:
  ```json
  {
    "title": "Movie Title",
    "release_date": "YYYY-MM-DD",
    "actors": [1, 2]
  }
  ```
- **Response**:
  - `status`: 200 if successful, 400 if failed
  - `success`: Boolean

#### PATCH /movies/<int:id>

- **Description**: Update a movie by ID.
- **Permissions**: `patch:movies`
- **Request Body**:
  ```json
  {
    "title": "Updated Title",
    "release_date": "YYYY-MM-DD",
    "actors": [1, 2]
  }
  ```
- **Response**:
  - `status`: 200 if successful, 400 if failed
  - `success`: Boolean

#### DELETE /movies/<int:id>

- **Description**: Delete a movie by ID.
- **Permissions**: `delete:movies`
- **Response**:
  - `status`: 200 if successful, 400 if failed
  - `success`: Boolean

### Actors

#### GET /actors

- **Description**: Fetch all actors.
- **Permissions**: `view:actors`
- **Response**:
  - `status`: 200
  - `data`: List of actors, each with `id`, `name`, `age`, and `gender`.

#### POST /actors

- **Description**: Add a new actor.
- **Permissions**: `post:actors`
- **Request Body**:
  ```json
  {
    "name": "Actor Name",
    "age": 30,
    "gender": "Male"
  }
  ```
- **Response**:
  - `status`: 200 if successful, 400 if failed
  - `success`: Boolean

#### PATCH /actors/<int:id>

- **Description**: Update an actor by ID.
- **Permissions**: `patch:actors`
- **Request Body**:
  ```json
  {
    "name": "Updated Name",
    "age": 31,
    "gender": "Female"
  }
  ```
- **Response**:
  - `status`: 200 if successful, 400 if failed
  - `success`: Boolean

#### DELETE /actors/<int:id>

- **Description**: Delete an actor by ID.
- **Permissions**: `delete:actors`
- **Response**:
  - `status`: 200 if successful, 400 if failed
  - `success`: Boolean

## Error Handling

Errors are returned as JSON objects with the following structure:

```json
{
  "status": 400,
  "success": false,
  "message": "Error message"
}
```

Common error status codes:

- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **500** - Internal Server Error

## Running the Application

Start the Flask application by running:

```bash
flask run
```

## Run Test Case

Start the Testing by running:

```bash
python -m unittest __test__.py
```

## Testing

To test the API, use a tool like Postman to make requests to each endpoint. Ensure to include a valid Auth0 token with the required permissions in the request headers.
