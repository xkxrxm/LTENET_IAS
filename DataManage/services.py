import os

import pandas as pd
from sqlalchemy.exc import DataError, IntegrityError

from app.database import engine


def upload_data_background(csv_path: str, table_name: str, chunk_size: int):
    try:
        reader = pd.read_csv(csv_path, chunksize=chunk_size)
        for chunk in reader:
            try:
                chunk.to_sql(table_name, con=engine, if_exists='append', chunksize=chunk_size, index=False)
            except Exception:
                for _, row in chunk.iterrows():
                    try:
                        row.to_frame().T.to_sql(table_name, con=engine, if_exists='append', index=False)
                    except DataError as e:
                        print(e.params)
                    except IntegrityError as e:
                        print(e.params)
    except Exception:
        raise
    finally:
        os.remove(csv_path)
