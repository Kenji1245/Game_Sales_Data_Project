import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import mplcursors

import psycopg2

# 1: Purpose is to find various information on data we retrieved. 

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

# Use pandas to run SQL and return a DataFrame
df = pd.read_sql("SELECT * FROM vg_sales;", conn)

# 6: Viewing data
print("\n1. Checking the top rows of data\n")
print(df.head())
print("\n 2.Checking the dispersion of the data and central tendency.\n")
print(df.describe())

# What is the top 100 global sales and how does rank affect the number of sales. 
# Top 100 Global Sales
def scatterPlot():
    top_sales_df = df.sort_values(by="global_sales", ascending=False,) # Sort the data by global sales in descending order
    top_100_sales = top_sales_df.head(100) # Select the top 100 global sales
    print(top_100_sales) # Shows table of the top 100 games

    top_100_sales
    rank = top_100_sales['rank']
    g_sales = top_100_sales['global_sales']
    na_sales = top_100_sales['na_sales']
    eu_sales = top_100_sales['eu_sales']
    jp_sales = top_100_sales['jp_sales']
    other_sales = top_100_sales['other_sales']

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
        sel.annotation.set_text(df['name'].iloc[i])
    

    plt.legend()  # Show the legend (it will display color and label)

    plt.xlabel('Rank')
    plt.ylabel('Global, NA, EU, JP, and othersl_Sales, (Millions $)')
    plt.title('Rank vs Sales (Global, NA, EU, JP, and others)')
    plt.show()

def hBarChart():
    top_sales_df = df.sort_values(by="global_sales", ascending=False,) # Sort the data by global sales in descending order
    top_20_sales = top_sales_df.head(20)
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
    unique_count = df['publisher'].nunique() # nunique() shows us the number of unique values there are on the column 'publisher'.
    print(unique_count) 

    # Get the top 10 most frequent unique values
    top_10 = df['publisher'].value_counts().head(10) # value_counts counts the occurrences of each unique value and head(10) gets the top 10 values.
    ten_most_frequent_publisher = top_10.reset_index() # reset_index() is used to move the index back into a regular column.
    print(ten_most_frequent_publisher) # top_10 shows us the top ten publisher and the number of games they have published. 
    
    x3 = ten_most_frequent_publisher['publisher']
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
    top_ten_years = df['year'].value_counts().head(10) # gets the top years that have released the most games frequently. 
    top_ten_years = top_ten_years.reset_index() # Moves the values onto a table.
    top_ten_years = top_ten_years.sort_values( by = 'year', ascending=True)

    x4 = top_ten_years['year']
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
    top_ten_years = df['year'].value_counts().tail(10) # gets the top years that have released the least games frequently. 
    top_ten_years = top_ten_years.reset_index() # Moves the values onto a table.
    top_ten_years = top_ten_years.sort_values( by = 'year', ascending=True) # rearrange the table within ascending order according to year.

    x5 = top_ten_years['year']
    y5 = top_ten_years['count']
    

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
    top_five_platforms = df['platform'].value_counts().head(5)
    top_five_platforms = top_five_platforms.reset_index()
    top_five_platforms = top_five_platforms.sort_values(by = "platform", ascending=True)

    print(top_five_platforms)

    x6 = top_five_platforms['platform']
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
    top_five_platforms = df['platform'].value_counts().head(5)
    top_five_platforms = top_five_platforms.reset_index()
    top_five_platforms = top_five_platforms.sort_values(by = "platform", ascending=True)

    print(top_five_platforms)

    x6 = top_five_platforms['platform']
    y6 = top_five_platforms['count']

    colour = ['gold', 'skyblue', 'lightcoral', 'lightgreen','silver']
    explode = (0.1,0,0,0,0) # Explodes the first slice for emphasis


    plt.figure(figsize=(8,8))
    plt.pie(y6, labels=x6, colors=colour, explode=explode,autopct='%1.1f%%', shadow= True) # autopct controls the number format for percentage and shows it, and shadow adds shadow for depth.
    plt.title('Five Most Frequent Platform')
    plt.axis('equal')
    plt.show()

def count_vs_globalSales_histo():
    count_vs_globalSales = df.sort_values(by="global_sales", ascending=False)

    y_values = count_vs_globalSales['global_sales']
    print(y_values)
    
    plt.figure(figsize=(8,6))
    plt.hist(y_values, bins=60, color = 'skyblue', edgecolor='black')
    plt.title('Global Sales')
    plt.xlabel('Games by Rank')
    plt.ylabel('Global Sales')
    plt.grid(True)
    plt.show()


def Genre_vs_count():
    # Get value counts
    genre_vs_count = df['genre'].value_counts()
    print(genre_vs_count)

    # colour
    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink',"wheat",'#4E79A7', '#F28E2B', '#E15759', '#76B7B2', ]

    # plot bar chart
    genre_vs_count.plot(kind='bar', color = colour)

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    # Show the plot
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.title('Genre of games that have been made the most')
    plt.show()

def platform_vs_count():
    # Get value count
    platform_vs_count = df['platform'].value_counts()
    print(platform_vs_count)

    # colour 
    colour = ["lightblue", "lightgreen", "lightcoral","lightskyblue", 'lightpink',"wheat",'#4E79A7', '#F28E2B', '#E15759', '#76B7B2', ]

    # plot bar chart
    platform_vs_count.plot(kind='bar', color = colour)

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    plt.xlabel('Platform')
    plt.ylabel('Count')
    plt.title('What platform do games get played the most')
    plt.show()
