.PHONY: help build up down logs migrate shell seed test lint format clean

help:
	@echo "IssuePilot Makefile Commands"
	@echo "============================"
	@echo "build          - Build Docker containers"
	@echo "up             - Start all services"
	@echo "down           - Stop all services"
	@echo "logs           - View logs"
	@echo "migrate        - Run Django migrations"
	@echo "makemigrations - Create Django migrations"
	@echo "shell          - Django shell"
	@echo "seed           - Seed demo data"
	@echo "test           - Run tests"
	@echo "lint           - Run linters"
	@echo "format         - Format code"
	@echo "clean          - Clean up containers and volumes"

build:
	docker compose build

up:
	docker compose up

up-d:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

shell:
	docker compose exec backend python manage.py shell

seed:
	docker compose exec backend python manage.py seed_demo_data

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

test:
	docker compose exec backend pytest

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm run test

lint:
	docker compose exec backend ruff check .
	docker compose exec backend black --check .
	cd frontend && npm run lint

format:
	docker compose exec backend ruff check --fix .
	docker compose exec backend black .
	cd frontend && npm run format

clean:
	docker compose down -v
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules
	rm -rf frontend/dist

# Local development (non-Docker)
dev-backend:
	cd backend && python manage.py runserver

dev-frontend:
	cd frontend && npm run dev

dev-celery:
	cd backend && celery -A config worker -l info

dev-celery-beat:
	cd backend && celery -A config beat -l info
