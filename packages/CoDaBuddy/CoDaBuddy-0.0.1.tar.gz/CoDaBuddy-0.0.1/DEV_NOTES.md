# Create postgres testdata


```bash
docker exec postgres /usr/bin/psql -Atx postgresql://postgres:mysupersavepw@localhost -c "CREATE DATABASE coda_ps_test;" && /usr/bin/psql -Atx postgresql://postgres:mysupersavepw@localhost/coda_ps_test -c "\
  BEGIN; \
  create schema coda_ps_test_scheme; \
  CREATE TABLE IF NOT EXISTS coda_ps_test_scheme.my_table(id integer PRIMARY KEY, firstname VARCHAR(32)); \
  INSERT INTO coda_ps_test_scheme.my_table(id,firstname) VALUES (1,'Anna2'); \
  INSERT INTO coda_ps_test_scheme.my_table(id,firstname) VALUES (2,'Thomas2'); \
  commit;"
```

## check data

```bash
docker exec postgres /usr/bin/psql -Atx postgresql://postgres:mysupersavepw@localhost/coda_ps_test -c "SELECT * FROM coda_ps_test_scheme.my_table;"
```
# Run Backupnow test

## docker

```bash
python3 CoDaBuddy/cli.py backup now --mode=docker --container-identifier=mysql --database-type=mysql --database-host=127.0.0.1 --database-user=root --database-names=coda_test
``` 

## kubernetes


```bash
python3 CoDaBuddy/cli.py backup now --mode=kubernetes --container-identifier=my-namespace/postgres01 --database-type=postgres --database-host=127.0.0.1 --database-user=postgres --database-names=coda_ps_test
``` 


# restore
```bash
python3 CoDaBuddy/cli.py restore kubernetes --namespace="my-namespace" --backup-name="postgresbackup_2022-01-28_10-23-46.sql" --workload-name="postgres01" --database-name="coda_ps_test"
```