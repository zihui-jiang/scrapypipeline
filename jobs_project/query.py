import psycopg2
import logging
import pandas as pd
import os

class Database:
    def __init__(self):
        self.postgres_conn = None

    def connect_postgres(self):
        try:
            self.postgres_conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB', 'mydatabase'),
                user=os.getenv('POSTGRES_USER', 'myuser'),
                password=os.getenv('POSTGRES_PASSWORD', 'mypassword'),
                host=os.getenv('POSTGRES_HOST', 'postgres')
            )
            print("Connected to PostgreSQL")

        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def fetch_data(self):
    
        if not self.postgres_conn:
            print("PostgreSQL connection is not established")
            return None
        
        cursor = self.postgres_conn.cursor()

        query = "SELECT * FROM raw_table;"
        try:
            df = pd.read_sql_query(query, self.postgres_conn)
            print("result: " + str(df))
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def close_postgres(self):
        if self.postgres_conn:
            self.postgres_conn.close()
            print("PostgreSQL connection closed")

    def export_to_csv(self, df, file_path):
        try:
            df.to_csv(file_path, index=False)
            print(f"Data exported to {file_path}")
        except Exception as e:
            print(f"Error exporting data to CSV: {e}")

if __name__ == "__main__":
    print("fetch data starts")
    db = Database()
    db.connect_postgres()
    data = db.fetch_data()
    
    if data is not None:
        print("fetch data ends")
        db.export_to_csv(data, 'processed_data.csv')
    db.close_postgres()