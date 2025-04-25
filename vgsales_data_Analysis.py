import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import mplcursors

import psycopg2

# 1: Purpose is to find various information on data we retrieved. 

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


query = "SELECT * FROM vg_sales;"

# Load data into a DataFrame
df = pd.read_sql_query(query, conn)

conn.close() # Closes the cursor. 


# 6: Viewing data
print("\n1. Checking the top rows of data\n")
print(df.head())
print("\n 2.Checking the dispersion of the data and central tendency.\n")
print(df.describe())

top_sales_df = df.sort_values(by="global_sales", ascending=False,) # Sort the data by global sales in descending order
top_sales_df.head(10)
print(top_sales_df.head(10))

# What is the top 100 global sales and how does rank affect the number of sales. 
# Top 100 Global Sales
def scatterPlot():
    top_sales_df = df.sort_values(by="Global_Sales", ascending=False,) # Sort the data by global sales in descending order
    top_100_sales = top_sales_df.head(100) # Select the top 100 global sales
    print(top_100_sales) # Shows table of the top 100 games

    top_100_sales
    rank = top_100_sales['Rank']
    g_sales = top_100_sales['Global_Sales']
    na_sales = top_100_sales['NA_Sales']
    eu_sales = top_100_sales['EU_Sales']
    jp_sales = top_100_sales['JP_Sales']
    other_sales = top_100_sales['Other_Sales']

    # plt.figure(figsize=(8,6))

    fig, ax = plt.subplots(figsize=(12, 8)) # Create the size of graph

    g_graph = ax.scatter(rank, g_sales, label='global' ,c = 'green',alpha=0.6, s = 20) # plots the points for global values 
    na_graph = ax.scatter(rank, na_sales, label='na' ,alpha=0.6, c = 'yellow', s = 20) # plots the points for north american values 
    eu_graph= ax.scatter(rank, eu_sales, label='eu' ,alpha=0.6, c = 'blue', s = 20) # plots the points for european values 
    jp_graph = ax.scatter(rank, jp_sales, label='jp' ,alpha=0.6, c = 'red', s = 20) # plots the points for japanese values 
    other_graph = ax.scatter(rank, other_sales, label='other' ,alpha=0.6, c = 'purple', s = 20) # plots the points for other values 

    graphs = [g_graph,na_graph,eu_graph,jp_graph,other_graph] # puts all the graphs on a list.

    # Attach names to the points
    cursor = mplcursors.cursor(graphs, hover=True) # Adds hover interactivity

    @cursor.connect("add")
    def on_add(sel):
        i = sel.index
        sel.annotation.set_text(df['Name'].iloc[i])
    

    plt.legend()  # Show the legend (it will display color and label)

    plt.xlabel('Rank')
    plt.ylabel('Global, NA, EU, JP, and othersl_Sales, (Millions $)')
    plt.title('Rank vs Sales (Global, NA, EU, JP, and others)')
    plt.show()

def hBarChart():
    top_sales_df = df.sort_values(by="global_sales", ascending=False,) # Sort the data by global sales in descending order
    top_20_sales = top_sales_df.head(20)
    print(top_20_sales)
    x2 = top_20_sales['global_sales']
    y2 = top_20_sales['name']
    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink',"wheat",'#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948']

    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7) # Add horizontal grid lines 
    plt.grid(True, axis='x', linestyle='--', linewidth=0.7, alpha=0.7) # Add vertical grid lines

    plt.barh(y2, x2, color=colour)
    plt.xlabel('Global_Sales ($ Millions)')
    plt.ylabel('Name')
    plt.title('Horizontal Bar Chart')

    plt.show()

def BarChart_Game_Publisher():
    unique_count = df['Publisher'].nunique() # nunique() shows us the number of unique values there are on the column 'publisher'.
    print(unique_count) 

    # Get the top 10 most frequent unique values
    top_10 = df['Publisher'].value_counts().head(10) # value_counts counts the occurrences of each unique value and head(10) gets the top 10 values.
    ten_most_frequent_publisher = top_10.reset_index() # reset_index() is used to move the index back into a regular column.
    print(ten_most_frequent_publisher) # top_10 shows us the top ten publisher and the number of games they have published. 
    
    x3 = ten_most_frequent_publisher['Publisher']
    y3 = ten_most_frequent_publisher['count']
    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink',"wheat",'#4E79A7', '#F28E2B', '#E15759', '#76B7B2']

    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7) # Add horizontal grid lines 
    plt.grid(True, axis='x', linestyle='--', linewidth=0.7, alpha=0.7) # Add vertical grid lines

    plt.bar(x3, y3, color=colour)
    plt.xlabel("Publisher")
    plt.ylabel("count")
    plt.title("Top ten Publisher by count")
    plt.xticks(rotation=45)
    plt.show()

def ten_most_frequent_years():
    top_ten_years = df['Year'].value_counts().head(10) # gets the top years that have released the most games frequently. 
    top_ten_years = top_ten_years.reset_index() # Moves the values onto a table.
    top_ten_years = top_ten_years.sort_values( by = 'Year', ascending=True)

    x4 = top_ten_years['Year']
    y4 = top_ten_years['count']

    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7) # Add horizontal grid lines 
    plt.grid(True, axis='x', linestyle='--', linewidth=0.7, alpha=0.7) # Add vertical grid lines

    print(top_ten_years)

    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink',"wheat",'#4E79A7', '#F28E2B', '#E15759', '#76B7B2']

    plt.bar(x4, y4, color=colour)
    plt.xlabel("Year")
    plt.ylabel("count")
    plt.title("Top ten Years that have released the most games")
    plt.xticks(x4,rotation=45) # x4 shows all the x values on graph and rotation = 45 rotates the year 45 degrees. 
    plt.show()

def ten_least_frequent_years():
    top_ten_years = df['Year'].value_counts().tail(10) # gets the top years that have released the least games frequently. 
    top_ten_years = top_ten_years.reset_index() # Moves the values onto a table.
    top_ten_years = top_ten_years.sort_values( by = 'Year', ascending=True) # rearrange the table within ascending order according to year.

    x5 = top_ten_years['Year']
    y5 = top_ten_years['count']
    print("here")
    print(type(x5))
    print(x5)

    new_x5 = [] # Place new string year values onto list.
    for year in x5: 
        new_year = str(year) # converts the num values into strings. 
        new_x5.append(new_year) # puts values into list. 
    

    print("here")
    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7) # Add horizontal grid lines 
    plt.grid(True, axis='x', linestyle='--', linewidth=0.7, alpha=0.7) # Add vertical grid lines

    print(top_ten_years)

    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink',"wheat",'#4E79A7', '#F28E2B', '#E15759', '#76B7B2']

    plt.bar(new_x5, y5, color=colour)
    plt.xlabel("Year")
    plt.ylabel("count")
    plt.title("Top ten Years that have released the least games")
    plt.xticks(new_x5,rotation=45) # x5 shows all the x values on graph and rotation = 45 rotates the year 45 degrees. 
    plt.show()

def top_five_frequent_Platform_barChart():
    top_five_platforms = df['Platform'].value_counts().head(5)
    top_five_platforms = top_five_platforms.reset_index()
    top_five_platforms = top_five_platforms.sort_values(by = "Platform", ascending=True)

    print(top_five_platforms)

    x6 = top_five_platforms['Platform']
    y6 = top_five_platforms['count']

    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink']

    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7) # Add horizontal grid lines 
    plt.grid(True, axis='x', linestyle='--', linewidth=0.7, alpha=0.7) # Add vertical grid lines

    plt.bar(x6, y6, color=colour)
    plt.xlabel('Platform')
    plt.ylabel('Count')
    plt.title('Five Most Frequent Platform')
    plt.xticks(x6)
    plt.show()

def top_five_frequent_Platform_pieChart():
    top_five_platforms = df['Platform'].value_counts().head(5)
    top_five_platforms = top_five_platforms.reset_index()
    top_five_platforms = top_five_platforms.sort_values(by = "Platform", ascending=True)

    print(top_five_platforms)

    x6 = top_five_platforms['Platform']
    y6 = top_five_platforms['count']

    colour = ['gold', 'skyblue', 'lightcoral', 'lightgreen','silver']
    explode = (0.1,0,0,0,0) # Explodes the first slice for emphasis


    plt.figure(figsize=(8,8))
    plt.pie(y6, labels=x6, colors=colour, explode=explode,autopct='%1.1f%%', shadow= True) # autopct controls the number format for percentage and shows it, and shadow adds shadow for depth.
    plt.title('Five Most Frequent Platform')
    plt.axis('equal')
    plt.show()

def count_vs_globalSales_histo():
    count_vs_globalSales = df.sort_values(by="Global_Sales", ascending=False)

    y_values = count_vs_globalSales['Global_Sales']
    print(y_values)
    
    plt.figure(figsize=(8,6))
    plt.hist(y_values, bins=60, color = 'skyblue', edgecolor='black')
    plt.title('Global Sales')
    plt.xlabel('Games by Rank')
    plt.ylabel('Global Sales')
    plt.grid(True)
    plt.show()


def count_vs_globalSales_histo():
    count_vs_globalSales = df.sort_values(by="Global_Sales", ascending=False)

    x_values = count_vs_globalSales['Global_Sales']
    filter_x_values = x_values[x_values < 50]
    
    plt.figure(figsize=(8,6))
    plt.hist(filter_x_values, bins=60, color = 'skyblue', edgecolor='black')
    plt.title('Global Sales')
    plt.xlabel('Games by Rank')
    plt.ylabel('Global Sales')
    plt.grid(True)
    plt.show()
