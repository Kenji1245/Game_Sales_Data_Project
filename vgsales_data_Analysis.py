import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


df = pd.read_csv(
    r"C:\Users\kegge\OneDrive\Desktop\Coding_Projects\Game Sales Data Project\vgsales.csv"
)

print(df.head)

df.info()

df.describe()


df.dropna(inplace=True) # All rows with missing values have been dropped

print(df.isnull().sum())

df.duplicated().sum() # No duplicate values. 


# Top 100 Global Sales
top_sales_df = df.sort_values(by="Global_Sales", ascending=False) # Sort the data by global sales in descending order
top_100_sales = top_sales_df.head(100) # Select the top 100 global sales
print(top_100_sales.head(20))

x = df['Rank']
y = df['Global_Sales']

plt.scatter(x.values,y.values, )
plt.show()



