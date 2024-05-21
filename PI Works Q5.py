import pandas as pd

url = "https://www.piworks.net/Upload/Document/Original/country_vaccination_stats.csv"
df = pd.read_csv(url)


def fill_missing_vaccinations(df):
    # Get the minimum daily vaccination per country
    min_vaccinations = df.groupby('country')['daily_vaccinations'].min().fillna(0)

    #function to fill missing values
    def fill_row(row):
        if pd.isna(row['daily_vaccinations']):
            return min_vaccations[row['country']]
        return row['daily_vaccinations']
    
    # Apply the function to the dataframe
    df['daily_vaccinations'] = df.apply(fill_row, axis=1)
    
    return df

df_filled = fill_missing_vaccinations(df)

# Save the filled dataset to a new CSV file
df_filled.to_csv('filled_country_vaccination_stats.csv', index=False)

# Print first few rows to verify
print(df_filled.head())
