.PHONY: build run clean run clean_run test clean_test make_migrations migrate

build:
	docker-compose build

run:
	docker-compose up

destroy:
	docker-compose down

clean_run: destroy build run

test:
	docker-compose run web pytest

clean_test: destroy build test

make_migrations:
	docker-compose run web alembic revision --autogenerate

migrate:
	docker-compose run web alembic upgrade head

bash:
	docker-compose run web bash