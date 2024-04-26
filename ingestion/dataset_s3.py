from ingestion.duck import set_s3_duck_conn
import pandas as pd


def get_dataset_from_s3(duck_conn, source: str) -> pd.DataFrame:
    conn = set_s3_duck_conn(duck_conn)
    query = build_google_play_query(source)
    result = conn.execute(query).df()
    return result


def build_google_play_query(source: str) -> str:
    return f"""

    SELECT 
    "App Name" as app_name,
    "App Id" as app_id,
    "Category" as category,
    "Rating" as rating,
    "Rating Count" as rating_count,
    "Installs" as installs,
    "Free" as free,
    "Price" as price,
    "Currency" as currency,
    "Size" as size,
    "Scraped Time" as timestamp
    FROM read_csv('{source}')
    """
