import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

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

# Top 100 Global Sales
def scatterPlot():
    top_sales_df = df.sort_values(by="Global_Sales", ascending=False,) # Sort the data by global sales in descending order
    top_100_sales = top_sales_df.head(100) # Select the top 100 global sales
    print(top_100_sales) # Shows table of the top 100 games

    top_100_sales
    x = top_100_sales['Rank']
    y = top_100_sales['Global_Sales']

    plt.figure(figsize=(8,6))

    plt.scatter(x.values,y.values, alpha=0.6, c = 'blue', s = 10)
    plt.xlabel('Rank')
    plt.ylabel('Global_Sales')
    plt.title('Rank vs Global Sales')
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
