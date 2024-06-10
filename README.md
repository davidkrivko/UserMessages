# FastAPI Service with PostgreSQL and Telegram Integration

## Project Overview
A FastAPI service integrated with PostgreSQL, featuring a role-based access control system. The service processes and saves incoming JSON requests and sends messages to Telegram.

## Features
- Role-Based Access Control (RBAC)
- User Authentication and Authorization with JWT
- Processing and Saving JSON Requests
- Telegram Messaging Integration

## Requirements
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- aiohttp
- JWT

## Project Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/davidkrivko/UserMessages.git


2. Run docker:
   ```sh
   docker-compose up -d


3. Run migrations:
   ```sh
   alembic upgrade head


4. Upload database data:
   ```sh
   psql -U <username> -d <dbname> -f dump.sql
