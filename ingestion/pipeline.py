from ingestion.dataset_s3 import get_dataset_from_s3
from ingestion.duck import write_to_s3_from_duckdb, create_table_from_dataframe, read_from_s3_as_duckdb_parquet
from ingestion.models import validate_dataframe, GooglePlaystore
import duckdb


def main():
    conn = duckdb.connect(database=':memory:', read_only=False)
    # Loading data from s3
    s3_dataset_base = "s3://datasets"
    name = "Google-Playstore"
    table_name = "playstore"
    source = f"{s3_dataset_base}/{name}.csv"
    dst = f"{s3_dataset_base}/"
    df = get_dataset_from_s3(conn, source=source)
    # Validate data
    validate_dataframe(df.head(), GooglePlaystore)
    # write data to
    create_table_from_dataframe(conn, table_name, "df")
    write_to_s3_from_duckdb(conn, table_name, dst, "timestamp")


if __name__ == "__main__":
    main()
