import mysql.connector
from config.config import MYSQL_CONFIG

def stage_to_mysql(df, table_name):

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    columns = ", ".join([f"`{col}` TEXT" for col in df.columns])
    cursor.execute(f"CREATE TABLE {table_name} ({columns})")

    for _, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(row))
        cursor.execute(
            f"INSERT INTO {table_name} VALUES ({placeholders})",
            tuple(row.astype(str))
        )

    conn.commit()
    conn.close()
    print(f"{table_name} staged in MySQL")

    if __name__ == "__main__":
     stage_to_mysql()