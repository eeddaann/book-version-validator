test:
	python -m pytest -v

start:
	cd webapp && flask run

docker-build-run:
	docker build -t bookversion . && docker run -p 5000:5000 bookversion
