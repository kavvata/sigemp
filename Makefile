build:
	docker compose build
up:
	docker compose up

tailwind:
	docker-compose exec web python manage.py tailwind start

migrate:
	docker-compose exec web python manage.py migrate

down:
	docker-compose down
