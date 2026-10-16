
import pandas as pd
import mysql.connector

# Read the CSV
csv_path = (
    "data/processed/smartphones_cleaned.csv"
)

df = pd.read_csv(csv_path)

# Convert pandas missing values to Python None,
# which MySQL Connector sends as SQL NULL.
df = df.astype(object).where(pd.notna(df), None)

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="smartphone_data_intelligence"
)

cursor = connection.cursor()

# Insert all 22 CSV columns; MySQL generates id.
columns = [
    "brand_name", "model", "price", "avg_rating",
    "5G_or_not", "processor_brand", "num_cores",
    "processor_speed", "battery_capacity",
    "fast_charging_available", "fast_charging",
    "ram_capacity", "internal_memory", "screen_size",
    "refresh_rate", "num_rear_cameras", "os",
    "primary_camera_rear", "primary_camera_front",
    "extended_memory_available", "resolution_height",
    "resolution_width"
]

column_sql = ", ".join(f"`{c}`" for c in columns)
placeholders = ", ".join(["%s"] * len(columns))

sql = f"""
INSERT INTO smartphones ({column_sql})
VALUES ({placeholders})
"""

# Clear old rows before importing.
cursor.execute("TRUNCATE TABLE smartphones")

# Convert each row into values for MySQL.
rows = []
for record in df[columns].itertuples(index=False, name=None):
    rows.append(tuple(
        None if pd.isna(value) else value
        for value in record
    ))

# Insert in batches.
batch_size = 100
for start in range(0, len(rows), batch_size):
    cursor.executemany(
        sql, rows[start:start + batch_size]
    )
    connection.commit()

print("CSV rows:", len(df))
cursor.execute("SELECT COUNT(*) FROM smartphones")
print("MySQL rows:", cursor.fetchone()[0])

cursor.close()
connection.close()
