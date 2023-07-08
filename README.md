# Flask-Mongo-CRUD
A simple Flask-MongoDB application to show and perform CRUD operations.

| The commands below are for Ubuntu OS

## Installation and Runnning the Server
There are 3 method you can use to setup and run the app
- [Normal Installation](#normal-installation)
- [Using `docker`](#using-docker)
- [Using `docker-compose`](#using-docker-compose)

### Normal Installation
- Create a virtual environment
    ```bash
    python3 -m venv .venv 
    ```
- Activate the virtual envrionment
    ```bash
    source .venv/bin/activate
    ```
- Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
- Create a `.env` file in root directory of project and add the MongoDB URI link in the file like
    ```
    MONGO_URI=mongodb://username:password@mongodbhost/database_name
    ```
- Now start the app
    ```bash
    flask run
    ```

### Using `docker`
Checkout the image at this [location](https://hub.docker.com/r/omaximani/flask-crud)
- Run the below command to start the container
    ```
    docker run \
    -p 5000:5000 \
    -e MONGO_URI="mongodb://username:password@mongodbhost/database_name" \ 
    omaximani/flask-crud
    ```

### Using `docker-compose`
- Make sure you have docker compose installed by running the below command
    ```bash
    docker compose version
    ```
- If above command ran successfully run below command to run the server and database ( database is not persistance since [`docker volume`](https://docs.docker.com/storage/volumes/) is not used )
    ```bash
    docker compose up
    ```

## API Documentaion
| Method | API Endpoint | API Body | Description |
| ------------- | ------------- | ------------- | ------------- |
| `POST` | `/users` | ```{ 'name', 'email', 'password' }``` | Creates a new user |
| `GET` | `/users/` | - | Retrieves all user from database |
| `GET` | `/users/<id>` | - | Retrieves a user form database according to `id` |
| `PUT` | `/users/<id>` | Specify the field which needs to be updates | Updates user field according to `id` |
| `DELETE` | `/users/<id>` | - | Deletes the user from database if exist according to `id` |


