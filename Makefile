.PHONY: build up down test lint clean

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down -v

logs:
	docker-compose logs -f

test:
	docker-compose run --rm webserver pytest tests/ -v

lint:
	docker-compose run --rm webserver flake8 dags/ tests/

clean:
	rm -rf logs/ .pytest_cache __pycache__