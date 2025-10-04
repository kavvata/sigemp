build:
	docker compose build
up:
	docker compose up
down:
	docker compose down

begin:
	docker compose exec web python manage.py migrate
	docker compose exec web python manage.py seed_2022
	docker compose exec web python manage.py loaddata ./core/fixtures/groups_and_permissions.json

begin_dev:
	docker compose exec web python manage.py seed_2022_fake

tailwind:
	docker compose exec web python manage.py tailwind start

migrate:
	docker compose exec web python manage.py migrate

shell:
	docker compose exec web python manage.py shell

collectstatic:
	docker compose exec web python manage.py collectstatic
