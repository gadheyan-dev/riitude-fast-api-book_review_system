# Book Review System

## Introduction

The project is a FastAPI-based application for managing books and their reviews. It provides RESTful endpoints for creating, updating, and deleting books, as well as adding reviews for specific books. The application uses SQLAlchemy for database interactions and has been designed with testability in mind. Additionally, the project includes a testing setup using pytest and in-memory SQLite databases to ensure a clean and isolated testing environment. The test suite covers the basic CRUD operations for both books and reviews, enhancing the reliability and robustness of the application.

![UI.](/assets/api_docs.png)


## Installation

This app can easily be installed using docker-compose command. Make sure docker is installed on your system before installing the app, you can view instructions [here](https://docs.docker.com/engine/install/).
To install go to the root directory where docker-compose.yml is present and do the following.
```bash
docker compose up --build
```


## Usage
Following command will start neccessary services for accessing swagger ui for the app. 
```bash
docker compose up
```
You can access the ui by visiting [http://0.0.0.0:8002/docs](localhost:8002/docs). 

![UI.](/assets/docker.png)
