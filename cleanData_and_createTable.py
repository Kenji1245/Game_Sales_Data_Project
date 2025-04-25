import pandas as pd

import psycopg2

# Pandas will be used to read, check, drop and clean data from the csv file.
# psycopg2 will be used to connect to the pgAdmin 4 sql database.

# The purpose of the cleanData_and_createTable file is to clean the data by identifying any rows containing missing values and dropping them. 
# Afterwards, a connection will be made to pgAdmin 4 sql database. Then SQL query execution will be done to create a table and insert values into that table. 
# This table will be called vg-sales. 

# 2: Data was collected from kaggle.

df = pd.read_csv(
        r"C:\Users\kegge\OneDrive\Desktop\Coding_Projects\Game Sales Data Project\vgsales.csv"
    )

# 3: Cleaning Data.

df.info() # Checking thhat each column is the correct type. 

print(df.describe()) # Checking the dispersion of the data and central tendency.


df.dropna(inplace=True) # All rows with missing values have been dropped.

df.isnull().sum()

df.duplicated().sum() # No duplicate values. 

# Save cleaned data to a new CSV (for use in COPY)
df.to_csv("cleaned_file.csv", index=False)

# 4. Connect to SQL Database and create a script to create a table.

# This code connects python to the SQL database in pgAdmin 4. 
# Replace with your own credentials
hostname = "localhost"
database = "analysis"
username = 'postgres'
pwd = 'Kennystar10!'
port_id = 5432

# Create a connection engine
conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id)

cur = conn.cursor() # Allows python code to execute PostgreSQL command in a database session.

# Create the main table
cur.execute(''' 
    CREATE TABLE IF NOT EXISTS vg_sales (
        Rank INTEGER PRIMARY KEY,
        Name varchar(200),
        Platform varchar(20),
        Year numeric(20,2),
        Genre varchar(20),
        Publisher varchar(100),
        NA_Sales numeric(20,2),
        EU_Sales numeric(20,2),
        JP_Sales numeric(20,2),
        Other_Sales numeric(20,2),
        Global_Sales numeric(20,2)
    );
''')

# Create a temporary table to hold the incoming data
cur.execute(''' 
    CREATE TABLE IF NOT EXISTS vg_sales_temp (
        Rank INTEGER PRIMARY KEY,
        Name varchar(200),
        Platform varchar(20),
        Year numeric(20,2),
        Genre varchar(20),
        Publisher varchar(100),
        NA_Sales numeric(20,2),
        EU_Sales numeric(20,2),
        JP_Sales numeric(20,2),
        Other_Sales numeric(20,2),
        Global_Sales numeric(20,2)
            
    );
''')


conn.commit() # Commit the create table execution.
print("vg_sales and vg_sales_temp Table created successfully.")

# 5. Open clean data and insert the data into SQL Database.  

with open("cleaned_file.csv", "r") as f:
    next(f)  # Skip header row
    cur.copy_expert("COPY vg_sales_temp (Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales) FROM STDIN WITH CSV ", f)

# Insert data from the temporary table into the main table, avoiding duplicates
cur.execute('''
    INSERT INTO vg_sales (Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales)
            
    SELECT Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales FROM vg_sales_temp
    
    ON CONFLICT (Rank) DO NOTHING;
''')

conn.commit()

cur.close() # Closes the cursor. 


conn.close() # Closes the cursor. 