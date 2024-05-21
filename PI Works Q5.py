import pandas as pd


url = "https://www.piworks.net/Upload/Document/Original/country_vaccination_stats.csv"
df = pd.read_csv(url)


def fill_missing_vaccinations(df):
    # Calculating the minimum daily vaccination per country
    min_vaccinations = df.groupby('country')['daily_vaccinations'].transform(lambda x: x.min(skipna=True))
    
    df['daily_vaccinations'] = df.apply(
        lambda row: min_vaccinations[row.name] if pd.isna(row['daily_vaccinations']) else row['daily_vaccinations'],
        axis=1
    ).fillna(0)
    
    return df


df_filled = fill_missing_vaccinations(df)


df_filled.to_csv('filled_country_vaccination_stats.csv', index=False)


print(df_filled.head())
