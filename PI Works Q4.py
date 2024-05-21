import pandas as pd

url = "https://www.piworks.net/Upload/Document/Original/country_vaccination_stats.csv"
df = pd.read_csv(url)

def fill_missing_vaccinations(df):
    # Get the minimum daily vaccination per country
    min_vaccinations = df.groupby('country')['daily_vaccinations'].min().fillna(0)

    #function to fill in missing values
    def fill_row(row):
        if pd.isna(row['daily_vaccinations']):
            return min_vaccinations[row['country']]
        return row['daily_vaccinations']
    
    df['daily_vaccinations'] = df.apply(fill_row, axis=1)
    
    return df

df_filled = fill_missing_vaccinations(df)


df_filled.to_csv('filled_country_vaccination_stats.csv', index=False)


print(df_filled.head())
