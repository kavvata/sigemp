build:
	docker compose build
up:
	docker compose up

tailwind:
	docker-compose exec web python manage.py tailwind start

down:
	docker-compose down
