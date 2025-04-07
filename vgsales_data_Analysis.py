import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import mplcursors

# 1: Purpose is to find various information on data we retrieved. This includes Read Data, Finding the top
# 100 video games, Genre VS Platform, Genre and Region.

# 2: Data was collected from kaggle.

df = pd.read_csv(
    r"C:\Users\kegge\OneDrive\Desktop\Coding_Projects\Game Sales Data Project\vgsales.csv"
)

df.head()

# 3: Cleaning Data.

df.info() # Checking thhat each column is the correct type. 

print(df.describe()) # Checking the dispersion of the data and central tendency.


df.dropna(inplace=True) # All rows with missing values have been dropped.

df.isnull().sum()

df.duplicated().sum() # No duplicate values. 


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
    plt.ylabel('Global, NA, EU, JP, and othersl_Sales')
    plt.title('Rank vs Sales (Global, NA, EU, JP, and others)')
    plt.show()

def hBarChart():
    top_sales_df = df.sort_values(by="Global_Sales", ascending=False,) # Sort the data by global sales in descending order
    top_20_sales = top_sales_df.head(20)
    x2 = top_20_sales['Global_Sales']
    y2 = top_20_sales['Name']

    plt.barh(y2, x2, color='skyblue')
    plt.xlabel('Global_Sales')
    plt.ylabel('Name')
    plt.title('Horizontal Bar Chart')

    plt.show()

def BarChart_Game_Publisher():
    unique_count = df['Publisher'].nunique() # nunique() shows us the number of unique values there are on the column 'publisher'.
    print(unique_count) 

    # Get the top 10 most frequent unique values
    top_10 = df['Publisher'].value_counts().head(10) # value_counts counts the occurrences of each unique value and head(10) gets the top 10 values.
    print(top_10) # top_10 shows us the top ten publisher and the number of games they have published. 

    # Plot bar chart
    plt.figure(figsize=(16, 10))
    top_10.plot(kind='bar', color='skyblue')
    plt.xlabel("Publisher")
    plt.ylabel("Count")
    plt.title("Top 10 Unique Values by Count")
    plt.xticks(rotation=45)
    plt.show()
