dockerdb:
	docker rm -f lunardb || true
	docker run --name=lunardb -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 -it -d postgres
	sleep 1
	poetry run alembic upgrade head

build:
	docker build -t lunar_api .

run: build
	docker rm -f lunar_api
	docker run --name=lunar_api --network=host -it -d lunar_api

logs:
	docker logs lunar_api -f