# Movel-View-Controller REST API using a Microservice Architecture

This is my version of the MVC REST API using a Microservice Architecture. I have used the following technologies:
 - Python
 - Go
 - PostgreSQL
 - Docker

## Requirements

You need Docker installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).

## How to run
Clone the project and follow the steps below:

1. Pull my PostgreSQL image from Docker Hub:
```docker pull acarnesecchi\postgres```
2. Modify the Dockerfile of the Flask and Go microservices to set up the environment variables or create a config.ini file with the PostgreSQL credentials.
3. Build the images:
```docker build -t flask ./movies```
```docker build -t go ./actors```
4. Run the containers:
```docker run -d -p 5432:5432 --name postgres acarnesecchi/postgres```
```docker run -d -p 5000:5000 --name flask flask```
```docker run -d -p 5001:5001 --name go go```
5. Check if the application is running:
```curl http://localhost:5000```
```curl http://localhost:5001```

## How to use

The PostgreSQL database is already populated with some data. You can modify the existing data or add new data using psql or the API endpoints:
 - ```localhost:5000/movies/create``` to add a new movie
 - ```localhost:5000/movies/<id>/delete``` to delete a movie
 - ```localhost:5000/movies/<id>/update``` to update a movie
 - ```localhost:5001/actors/create``` to add a new actor
 - ```localhost:5001/actors/<id>/delete``` to delete an actor
 - ```localhost:5001/actors/<id>/update``` to update an actor
