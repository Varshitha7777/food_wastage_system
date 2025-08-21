import sqlite3
import pandas as pd

# Connect
conn = sqlite3.connect("food.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Drop existing tables
cursor.executescript("""
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS food_listings;
DROP TABLE IF EXISTS receivers;
DROP TABLE IF EXISTS providers;
""")

# Create tables with schema
cursor.executescript("""
CREATE TABLE providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
);

CREATE TABLE receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    City TEXT,
    Contact TEXT
);

CREATE TABLE food_listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT,
    Quantity INTEGER,
    Expiry_Date DATE,
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers (Provider_ID)
);

CREATE TABLE claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID) REFERENCES food_listings (Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers (Receiver_ID)
);
""")

# Load CSVs
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food_listings = pd.read_csv("data/food_listings_data.csv", parse_dates=["Expiry_Date"])
claims = pd.read_csv("data/claims_data.csv", parse_dates=["Timestamp"])

# Insert data
providers.to_sql("providers", conn, if_exists="append", index=False)
receivers.to_sql("receivers", conn, if_exists="append", index=False)
food_listings.to_sql("food_listings", conn, if_exists="append", index=False)
claims.to_sql("claims", conn, if_exists="append", index=False)

conn.commit()
conn.close()
print("✅ Database created successfully with schema + constraints!")
