# 🛒 iCash Supermarket System

This repository implements a small microservices demo for the iCash SuperMarket Management system. It includes:
- cashier service
- owner service
- PostgreSQL DB with initial data (loaded from the provided CSVs)

  <img width="598" height="928" alt="image" src="https://github.com/user-attachments/assets/3fa5943d-d55d-44a0-8763-dca5409a70ba" />
  <img width="1192" height="837" alt="image" src="https://github.com/user-attachments/assets/4eccfce5-faff-4a31-a3e0-79ab37fb7e4a" />



---

## ✨ Features

### Cashier Service (POS)
- Create purchases
- Identify existing customers or create new ones automatically
- Calculate totals and validate items
- Store purchases in the database

### Owner Dashboard Service
- Unique buyers analytics
- Loyal buyers (based on number of purchases)
- Top-selling products with tie support

### System Highlights
- Microservices architecture (Cashier + Owner)
- FastAPI backend with SQLAlchemy ORM
- PostgreSQL database with initial CSV-based data loading
- Dockerized services using `docker-compose`
- Full structured logging across services
- Clean, modular controllers/services design

---

# 📦 Quick Start (Docker)

## Run the entire system
```bash
docker-compose up --build
```

This starts:
- `cashier` service  
- `owner` service  
- PostgreSQL database  
- Initialization scripts (CSV → DB)

### Access
- **Cashier UI**: http://localhost:8000/ui
- **Owner Dashboard**: http://localhost:8001/ui

---

# 🚀 Architecture

```
                                +----------------------+
                                |      FRONTEND UI     |
                                |  (HTML / JS Fetch)   |
                                +----------+-----------+
                                           |
                                           | HTTP (REST)
                             _ _ _ _ _ _ _ | _ _ _ _ _ _  
                            |                           |
                            |                           |
                            v                           v
       +---------------------------+        +---------------------------+
       |     Cashier Service       |        |      Owner Service        |
       |  (FastAPI app on :8000)  |        |  (FastAPI app on :8001)   |
       +-------------+-------------+        +-------------+-------------+
                     |                                      |
                     | SQLAlchemy / DB session              | SQLAlchemy / DB session
                     |                                      |
                     v                                      v
               +-------------------------------------------------+
               |                PostgreSQL DB                   |
               |  - tables: users, products, purchases, etc.     |
               |  - initial data loaded from CSVs on start       |
               +-------------------------------------------------+
```

---

# 🔌 API Endpoints

## Cashier Service
| Method | Endpoint      | Description |
|--------|---------------|-------------|
| POST   | `/purchase`   | Create a new purchase |

### Example Request
```json
{
  "supermarket_id": "SMKT001",
  "user_id": null,
  "items_list": ["Milk", "Bread"]
}
```

---

## Owner Dashboard Service

| Method | Endpoint          | Description |
|--------|-------------------|-------------|
| GET    | `/unique-buyers`  | Count of unique customers |
| GET    | `/loyal-buyers`   | Customers with the most purchases |
| GET    | `/top-products`   | Most frequently purchased products |

---

# 📜 Logging

All services emit structured logs to **stdout**, including:
- Timestamps  
- Log level  
- Exception tracebacks (via `logger.exception`)  
- Debug logs for data processing  

View logs for a specific service:
```bash
docker-compose logs -f cashier
docker-compose logs -f owner
```

---


## 🛠 Technologies Used

### Backend
- **FastAPI** – Web framework for building RESTful APIs quickly and efficiently  
- **Python 3.11+** – Core programming language  
- **SQLAlchemy ORM** – Object Relational Mapper for working with PostgreSQL  
- **Pydantic** – Data validation and settings management

### Database
- **PostgreSQL** – Relational database for storing users, purchases, and products  

### Microservices & Architecture
- **Microservices Architecture** – Separate services for Cashier and Owner Dashboard  
- **Docker & Docker Compose** – Containerization and orchestration of services and database  
- **REST API** – Communication between frontend and backend services

### Frontend
- **HTML + JavaScript (Fetch API)** – Lightweight frontend for interacting with backend services

### DevOps / Logging
- **Structured logging** – Timestamps, log levels, exception tracebacks  
- **Docker Compose commands** – Easy startup and log monitoring per service

---

# 🎉 Enjoy the Project  
Pull requests and improvements are welcome!
