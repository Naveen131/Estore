# Estore

This project is a simple RESTful API for an e-commerce platform built with Django and Dockerized for local development. The API allows users to view products, add products, and place orders.

---

## Features

- **Endpoints**:
  - `GET /products`: Retrieve a list of available products.
  - `POST /products`: Add a new product.
  - `POST /orders`: Place an order.
- **Stock Management**: Validates and updates product stock when orders are placed.
- **User Management**: Supports JWT-based authentication.
- **Dockerized**: Fully configured for running locally using Docker.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Build and Start Containers

Build and start the application using Docker Compose:

```bash
docker-compose up --build
```

This command will:
- Build the Docker image.
- Start the Django server on `http://localhost:8000`.

### 3. Apply Database Migrations

Run the following command to set up the database:

```bash
docker-compose exec web python manage.py migrate
```

### 4. Create a Superuser (Optional)

To access the Django admin panel, create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application

Visit `http://localhost:8000` in your browser. The following endpoints are available:

- **Products**:
  - `GET /products`
  - `POST /products`
- **Orders**:
  - `POST /orders`
- **Admin Panel**: `http://localhost:8000/admin`

---

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── settings.py
│   └── migrations/
```

- **Dockerfile**: Configuration for building the Docker image.
- **docker-compose.yml**: Defines the services and networks for the application.
- **requirements.txt**: Python dependencies for the project.
- **app/**: Main Django application directory.

---

## Running Tests

Run unit tests inside the container:

```bash
docker-compose exec web python manage.py test
```

---

## Troubleshooting

### Common Issues

1. **Server Stuck on "Watching for file changes with StatReloader":**
   - Ensure you are visiting `http://localhost:8000` in the browser.
   - Check container logs:
     ```bash
     docker-compose logs web
     ```

2. **Database Errors:**
   - Ensure migrations are applied:
     ```bash
     docker-compose exec web python manage.py migrate
     ```

3. **Changes Not Reflecting:**
   - Restart the containers:
     ```bash
     docker-compose down
     docker-compose up --build
     ```

---

## Notes

- For local development, the database uses SQLite.
- The project is designed for local testing and development only.

---

## Author

Developed by Naveen Chaudhary.

