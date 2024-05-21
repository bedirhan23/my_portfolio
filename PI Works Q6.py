import pandas as pd


url = "https://www.piworks.net/Upload/Document/Original/country_vaccination_stats.csv"
df = pd.read_csv(url)


def fill_missing_vaccinations(df):
    # Get the minimum daily vaccination per country
    min_vaccinations = df.groupby('country')['daily_vaccinations'].min().fillna(0)

    #function to fill missing values
    def fill_row(row):
        if pd.isna(row['daily_vaccinations']):
            return min_vaccinations[row['country']]
        return row['daily_vaccinations']
    
    # Apply the function to the dataframe
    df['daily_vaccinations'] = df.apply(fill_row, axis=1)
    
    return df


df_filled = fill_missing_vaccinations(df)


df_filled.to_csv('filled_country_vaccination_stats.csv', index=False)

def top_3_countries(df):
    # Calculate the median daily vaccination per country
    median_vaccinations = df.groupby('country')['daily_vaccinations'].median()
    
    # Sort the countries by median daily vaccination in descending order and get top 3
    top_3 = median_vaccinations.sort_values(ascending=False).head(3)
    
    return top_3

# Get the top-3 countries
top_3 = top_3_countries(df_filled)

# Print the result
print("Top-3 countries with the highest median daily vaccination numbers:")
print(top_3)

# Output the results
top_3.to_csv('top_3_countries_median_vaccination.csv', header=True)
