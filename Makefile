build:
	docker compose build
up:
	docker compose up
down:
	docker-compose down

tailwind:
	docker-compose exec web python manage.py tailwind start

migrate:
	docker-compose exec web python manage.py migrate

shell:
	docker-compose exec web python manage.py shell

collectstatic:
	docker-compose exec web python manage.py collectstatic
