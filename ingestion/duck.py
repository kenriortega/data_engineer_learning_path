import pandas as pd


def set_s3_duck_conn(duckdb_con):
    duckdb_con.execute("""
            INSTALL httpfs;
            LOAD httpfs;
            SET s3_region='us-east-1';
            SET s3_access_key_id='admin';
            SET s3_secret_access_key='password';
            SET s3_endpoint='192.168.1.105:9000';
            SET s3_use_ssl=false;
            SET s3_url_style='path';
        """)

    return duckdb_con


def create_table_from_dataframe(duckdb_con, table_name: str, dataframe: str):
    duckdb_con.sql(
        f"""
        CREATE TABLE {table_name} AS 
            SELECT *
            FROM {dataframe}
        """
    )


def write_to_s3_from_duckdb(
        duckdb_con, table: str, s3_path: str, timestamp_column: str
):
    duckdb_con.sql(
        f"""
        COPY (
            SELECT *,
                YEAR({timestamp_column}) AS year, 
                MONTH({timestamp_column}) AS month 
            FROM {table}
        ) 
        TO '{s3_path}/{table}' 
        (FORMAT PARQUET, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE 1, COMPRESSION 'ZSTD', ROW_GROUP_SIZE 1000000);
    """
    )


def read_from_s3_as_duckdb_parquet(duckdb_con, ):
    result = duckdb_con.sql(f"SELECT COUNT(*) FROM 's3://datasets/playstore/year=2021/month=6/data_0.parquet';")
    print(result)


def export_df_to_csv_local(duckdb_con, df: str, path_csv: str):
    duckdb_con.sql(f"COPY (select * from {df}) TO '{path_csv}'")
