up:
	docker-compose up

tailwind:
	docker-compose exec web pipenv run python manage.py tailwind start

down:
	docker-compose down
