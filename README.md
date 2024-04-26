# Documentation


## Dependencies

```sh

pip install "pyiceberg[s3fs,hive,sql-sqlite,duckdb,pyarrow]"
```

```yaml

version: "3.7"
name: etl
networks:
  data_lakehouse:
    driver: bridge
volumes:
  redpanda-0: null
services:
  postgres:
    image: 'postgres:latest'
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ikoko
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - data_lakehouse
  minio:
    image: minio/minio
    container_name: minio
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
    networks:
      - data_lakehouse
    ports:
      - 9001:9001
      - 9000:9000
    command: ["server", "/data", "--console-address", ":9001"]

  mc:
    depends_on:
      - minio
    image: minio/mc
    networks:
      - data_lakehouse
    container_name: mc
    entrypoint: >
      /bin/sh -c "
      until (/usr/bin/mc config host add minio http://minio:9000 admin password) do echo '...waiting...' && sleep 1; done;
      /usr/bin/mc rm -r --force minio/warehouse;
      /usr/bin/mc mb minio/warehouse;
      tail -f /dev/null
      " 
  # Nessie Catalog Server Using In-Memory Store
  nessie:
    image: projectnessie/nessie:latest
    container_name: nessie
    networks:
      - data_lakehouse
    ports:
      - 19120:19120
  rest:
    image: tabulario/iceberg-rest
    container_name: iceberg-rest
    networks:
      - data_lakehouse
    ports:
      - 8181:8181
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
      - CATALOG_WAREHOUSE=s3://warehouse/
      - CATALOG_IO__IMPL=org.apache.iceberg.aws.s3.S3FileIO
      - CATALOG_S3_ENDPOINT=http://minio:9000

```

```python
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.catalog.rest import RestCatalog

warehouse_path = "./warehouse"
catalog = SqlCatalog(
    "sqlite",
    **{
        "uri": f"sqlite:///{warehouse_path}/pyiceberg_catalog.db",
        "warehouse": f"file://{warehouse_path}",
    },
)
catalog = RestCatalog(
    "docs",
    **{
        "uri": "http://192.168.1.105:8181",
        "s3.endpoint": "http://192.168.1.105:9000",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": "admin",
        "s3.secret-access-key": "password"
    },
)
```

## Resources
- [https://py.iceberg.apache.org/api/#create-a-table](https://py.iceberg.apache.org/api/#create-a-table)
- [https://py.iceberg.apache.org/#installation](https://py.iceberg.apache.org/#installation)
- [https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps?resource=download](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps?resource=download)
- [https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps](https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps)
- [https://jira.readthedocs.io/](https://jira.readthedocs.io/)
- [https://documenter.getpostman.com/view/8765260/TzzHnDGw#00479c80-ae16-4bcd-90e9-96a9649b68d6](https://documenter.getpostman.com/view/8765260/TzzHnDGw#00479c80-ae16-4bcd-90e9-96a9649b68d6)