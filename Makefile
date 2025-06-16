build:
	docker compose build --no-cache

runserver:
	docker compose run --rm --build --service-ports --remove-orphans web python src/manage.py runserver 0.0.0.0:8000

migrate:
	docker compose run --rm web python src/manage.py migrate

makemigrations:
	docker compose run --rm web python src/manage.py makemigrations

run_bash:
	docker compose run --rm web python src/manage.py shell_plus --ipython

test:
	docker compose run --rm --remove-orphans web pytest
