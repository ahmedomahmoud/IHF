# IHF Championship Data Management System

This project is a backend system designed to manage data for handball championships, including teams, players, matches, and detailed play-by-play actions. It leverages PostgreSQL as the single source of truth, combining structured relational data with flexible JSONB fields to store high-volume, semi-structured event data.

## Features

*   **User Authentication:** Secure user registration and login with JWT-based authentication.
*   **Championship Management:** Create, retrieve, and manage championship details.
*   **Team Management:** Create, retrieve, and manage team information.
*   **Match Management:** Store and retrieve match details, scores, and statistics.
*   **Player Management:** Manage player information and their statistics within matches.
*   **CP File Parsing:** Automated parsing of `.CP` files to extract championship, match, and detailed play-by-play action data.
*   **Play-by-Play Actions:** Efficient storage and retrieval of granular match actions (e.g., goals, assists, fouls) 

## Technologies Used

*   **Backend Framework:** FastAPI (Python)
*   **Relational Database:** PostgreSQL
*   **ORM (Relational):** SQLAlchemy
*   **Authentication:** JWT (JSON Web Tokens)
*   **Environment Management:** `python-dotenv`
*   **Data Parsing:** Custom parser for `.CP` files

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd ihf
```

### 2. Set up Environment Variables

Create a `.env` file in the root directory of the project based on the `.env.example` file. This file will contain your database connection strings and other sensitive information.

```ini
SECRET_KEY="your_secret_key"

DB_HOST=your_db_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
```

*   Replace placeholders with your actual database credentials and a strong secret key.

### 3. Install Dependencies

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Database Setup

#### PostgreSQL (Relational Database)

Ensure your PostgreSQL server is running and accessible with the credentials provided in your `.env` file. The database schema is defined in `schema.png` and is managed by SQLAlchemy.

#### MongoDB (NoSQL Database)

Ensure your MongoDB instance is running and accessible. The `pbp_collection` will be automatically created when data is first inserted.

### 5. Run the Application

```bash
cd app
uvicorn main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000` (or similar, depending on your Uvicorn configuration).

## Docker

To build and run the application using Docker, follow these steps:

1.  **Build the Docker image:**

    ```bash
    docker compose build .
    ```

### Docker Compose

To run the application and its database dependencies using Docker Compose, follow these steps:

1.  **Ensure you have a `.env.docker` file with the required environment variables.**

2.  **Run Docker Compose:**

    ```bash
    docker compose up -d
    ```

    This will start the FastAPI application, PostgreSQL database, and MongoDB in detached mode.

3.  **To stop the services:**

    ```bash
    docker-compose down
    ```

## API Documentation

### Authentication

#### `POST /auth/register`

*   **Description:** Registers a new user.
*   **Request Body (`UserCreate`):**
    ```json
    {
        "first_name": "string",
        "last_name": "string",
        "username": "string",
        "password": "string"
    }
    ```
*   **Responses:**
    *   `201 Created`: User registered successfully.
        ```json
        {
            "message": "User registered successfully",
            "user_id": "string"
        }
        ```
    *   `400 Bad Request`: Username already exists.

#### `POST /auth/login`

*   **Description:** Logs in a user and returns an access token.
*   **Request Body (`UserLogin`):**
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
*   **Responses:**
    *   `200 OK` (`Token`):
        ```json
        {
            "access_token": "string",
            "token_type": "bearer"
        }
        ```
    *   `400 Bad Request`: Invalid username or password.

---

### Championships

#### `POST /championships/{championship_id}/upload-cp-file/`

*   **Description:** Uploads and processes a `.CP` file for a specific championship. This endpoint requires authentication.
*   **Path Parameters:**
    *   `championship_id` (integer): The ID of the championship.
*   **File Upload:**
    *   `file`: The `.CP` file to upload.
*   **Responses:**
    *   `200 OK`:
        ```json
        {
            "message": "File uploaded and processed for championship '{championship_id}' successfully."
        }
        ```
    *   `404 Not Found`: Championship not found.
    *   `500 Internal Server Error`: An error occurred while processing the file.

#### `GET /championships`

*   **Description:** Retrieves a list of all championships.
*   **Responses:**
    *   `200 OK` (List[`ChampionshipOut`]): A list of championship objects.

#### `GET /championships/{championship_id}`

*   **Description:** Retrieves a specific championship by its ID.
*   **Path Parameters:**
    *   `championship_id` (integer): The ID of the championship.
*   **Responses:**
    *   `200 OK` (`ChampionshipOut`): The championship object.
    *   `404 Not Found`: Championship not found.

#### `GET /championships/name/{championship_name}`

*   **Description:** Retrieves a specific championship by its name.
*   **Path Parameters:**
    *   `championship_name` (string): The name of the championship.
*   **Responses:**
    *   `200 OK` (`ChampionshipOut`): The championship object.
    *   `404 Not Found`: Championship not found.

#### `POST /championships`

*   **Description:** Creates a new championship. This endpoint requires authentication.
*   **Request Body (`ChampionshipCreate`):**
    ```json
    {
        "name": "string",
        "description": "string (optional)",
        "start_date": "date",
        "end_date": "date"
    }
    ```
*   **Responses:**
    *   `201 Created` (`ChampionshipOut`): The newly created championship object.

#### `PUT /championships/{champ_id}`

*   **Description:** Updates a championship. This endpoint requires authentication.
*   **Path Parameters:**
    *   `champ_id` (integer): The ID of the championship to update.
*   **Request Body (`ChampionshipUpdate`):**
    ```json
    {
        "name": "string (optional)",
        "description": "string (optional)",
        "start_date": "date (optional)",
        "end_date": "date (optional)"
    }
    ```
*   **Responses:**
    *   `200 OK` (`ChampionshipOut`): The updated championship object.
    *   `404 Not Found`: Championship not found.
    *   `400 Bad Request`: Another championship with the same name already exists.

#### `POST /championships/{champ_id}/teams`

*   **Description:** Links teams to a championship. This endpoint requires authentication.
*   **Path Parameters:**
    *   `champ_id` (integer): The ID of the championship.
*   **Request Body (`TeamIDs`):**
    ```json
    {
        "team_ids": [
            "integer"
        ]
    }
    ```
*   **Responses:**
    *   `200 OK` (`championshipout_linked`): The championship with linked teams.
    *   `404 Not Found`: Championship or Team not found.

#### `DELETE /championships/{champ_id}`

*   **Description:** Deletes a championship. This endpoint requires authentication.
*   **Path Parameters:**
    *   `champ_id` (integer): The ID of the championship to delete.
*   **Responses:**
    *   `200 OK`:
        ```json
        {
            "message": "Championship deleted successfully"
        }
        ```
    *   `404 Not Found`: Championship not found.

---

### Teams

#### `GET /teams`

*   **Description:** Retrieves a list of all teams.
*   **Responses:**
    *   `200 OK` (List[`TeamOut`]): A list of team objects.

#### `GET /teams/{team_id}`

*   **Description:** Retrieves a specific team by its ID.
*   **Path Parameters:**
    *   `team_id` (integer): The ID of the team.
*   **Responses:**
    *   `200 OK` (`TeamOut`): The team object.
    *   `404 Not Found`: Team not found.

#### `GET /teams/abbreviation/{abbreviation}`

*   **Description:** Retrieves a specific team by its abbreviation.
*   **Path Parameters:**
    *   `abbreviation` (string): The abbreviation of the team.
*   **Responses:**
    *   `200 OK` (`TeamOut`): The team object.
    *   `404 Not Found`: Team not found.

#### `POST /teams`

*   **Description:** Creates a new team. This endpoint requires authentication.
*   **Request Body (`TeamCreate`):**
    ```json
    {
        "name": "string",
        "abbreviation": "string"
    }
    ```
*   **Responses:**
    *   `201 Created` (`TeamOut`): The newly created team object.

#### `PUT /teams/{team_id}`

*   **Description:** Updates a team. This endpoint requires authentication.
*   **Path Parameters:**
    *   `team_id` (integer): The ID of the team to update.
*   **Request Body (`TeamUpdate`):**
    ```json
    {
        "name": "string (optional)",
        "abbreviation": "string (optional)"
    }
    ```
*   **Responses:**
    *   `200 OK` (`TeamOut`): The updated team object.
    *   `404 Not Found`: Team not found.
    *   `400 Bad Request`: Another team with the same name or abbreviation already exists.

#### `DELETE /teams/{team_id}`

*   **Description:** Deletes a team. This endpoint requires authentication.
*   **Path Parameters:**
    *   `team_id` (integer): The ID of the team to delete.
*   **Responses:**
    *   `200 OK` (`TeamOut`): The deleted team object.
    *   `404 Not Found`: Team not found.

---

### Matches

#### `GET /championships/{championship_id}/matches`

*   **Description:** Retrieves a list of all matches associated with a specific championship.
*   **Path Parameters:**
    *   `championship_id` (integer): The unique identifier for the championship.
*   **Responses:**
    *   `200 OK` (`list[MatchBaseOut]`): An array of match objects. If the championship has no matches, this will be an empty array `[]`.
    *   `404 Not Found`: The championship with the specified ID was not found.

#### `GET /matches/{match_id}/score`

*   **Description:** Retrieves the score for a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The ID of the match.
*   **Responses:**
    *   `200 OK` (`MatchScoreOut`): The match score object.
    *   `404 Not Found`: Match not found.

#### `GET /matches/{match_id}/stats`

*   **Description:** Retrieves the statistics for a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The ID of the match.
*   **Responses:**
    *   `200 OK` (`MatchStatesOut`): The match statistics object.
    *   `404 Not Found`: Match not found.

#### `GET /matches/{match_id}/referees`

*   **Description:** Retrieves the referees for a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The ID of the match.
*   **Responses:**
    *   `200 OK` (List[`RefereeWithRoleOut`]): A list of referee objects with their roles.
    *   `404 Not Found`: Referees not found for this match.

---

### Players

#### `GET /teams/{team_id}/players`

*   **Description:** Retrieves a list of players for a specific team.
*   **Path Parameters:**
    *   `team_id` (integer): The ID of the team.
*   **Responses:**
    *   `200 OK` (List[`PlayerOut`]): A list of player objects.
    *   `404 Not Found`: Players not found for this team.

#### `GET /matches/{match_id}/teams/{team_id}/players/stats`

*   **Description:** Retrieves the statistics for all players of a specific team in a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The ID of the match.
    *   `team_id` (integer): The ID of the team.
*   **Responses:**
    *   `200 OK` (List[`PlayerStatsOut`]): A list of player statistics objects.
    *   `404 Not Found`: Player stats not found for this team in this match.

#### `GET /matches/{match_id}/players/stats`

*   **Description:** Retrieves the statistics for all players in a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The ID of the match.
*   **Responses:**
    *   `200 OK` (List[`PlayerStatsOut`]): A list of player statistics objects.
    *   `404 Not Found`: Player stats not found for this match.

#### `GET /matches/{match_id}/teams/{team_id}/players/{player_id}/stats`

*   **Description:** Retrieves the statistics for a specific player of a specific team in a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The ID of the match.
    *   `team_id` (integer): The ID of the team.
    *   `player_id` (integer): The ID of the player.
*   **Responses:**
    *   `200 OK` (`PlayerStatsOut`): The player statistics object.
    *   `404 Not Found`: Player stats not found for this player in this match.

---

### Play-by-Play

#### `GET /matches/match_id/actions/page/{page_no}`

*   **Description:** Retrieves a paginated list of play-by-play actions for a specific match.
*   **Path Parameters:**
    *   `match_id` (integer): The id for the game.
    *   `page_no` (integer): The page number for pagination.
*   **Responses:**
    *   `200 OK` (List[`Action`]): A list of action objects.
    *   `404 Not Found`: Match not found.


## Database Schema

The relational database schema for PostgreSQL is visually represented below:

![Database Schema](schema.png)

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

