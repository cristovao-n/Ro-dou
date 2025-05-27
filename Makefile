.PHONY: run
run: \
create-logs-dir \
setup-containers

create-logs-dir:
	mkdir -p ./mnt/airflow-logs -m a=rwx

setup-containers:
	docker compose up -d --force-recreate --remove-orphans

.PHONY: down
down:
	docker compose down

.PHONY: tests
tests:
	docker exec airflow-webserver sh -c "cd /opt/airflow/tests/ && pytest -vvv --color=yes"
