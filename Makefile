dockerdb:
	docker rm -f lunardb || true
	mkdir -p data
	docker run --name=lunardb -e POSTGRES_HOST_AUTH_METHOD=trust -v data:/var/lib/postgresql/data -p 5431:5432 -it -d postgres
	sleep 1
	poetry run alembic upgrade head

build:
	docker build -t lunar_api .

rundev: build
	docker rm -f lunar_api || true
	docker run --name=lunar_api --network=host -it -d lunar_api

runprod: build
	docker rm -f lunar_api || true
	docker run --name=lunar_api --network=host -it -d lunar_api
logs:
	docker logs lunar_api -f

devdb: dockerdb
	python scripts/add_lunar_events.py
	psql -h localhost -p 5431 -U postgres -d postgres

rerundev: build rundev logs
