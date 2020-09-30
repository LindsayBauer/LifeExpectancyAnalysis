from pathlib import Path

import pandas as pd
from scipy.stats import mstats

SRC_DIR = Path.cwd().parent

def interpolate_df(df, feature):
    ''' Interpolate DataFrame df via specified feature and return it. '''
    interpolated_data = []
    for elem in df[feature].unique():
        filtered_data = df[df[feature].eq(elem)].copy()
        for column in list(filtered_data.columns)[3:]:
            # Set NaNs to the column average for specified feature
            filtered_data[column] = filtered_data[column].fillna(
                filtered_data[column].mean()).copy()
        interpolated_data.append(filtered_data)
    df = pd.concat(interpolated_data).copy()
    return df


def get_df():
    ''' Return pre-processed DataFrame. '''
    # Read in raw data
    df = pd.read_csv(SRC_DIR / "Data.csv")

    # Standardize format of feature names
    original_feature_names = list(df.columns)
    new_feature_names = []
    for name in original_feature_names:
        new_feature_names.append(name.strip().replace(
            '  ', ' ').replace(' ', '_').lower())
    df.columns = new_feature_names

    # Change feature name to be more accurately descriptive
    df.rename(
        columns={"thinness_1-19_years": "thinness_10-19_years"}, inplace=True)

    # Shorten name of some of the longest country names
    df['country'] = df['country'].replace(
        {"United Kingdom of Great Britain and Northern Ireland": "United Kingdom"})
    df['country'] = df['country'].replace(
        {"Democratic People's Republic of Korea": "North Korea"})
    df['country'] = df['country'].replace(
        {"Venezuela (Bolivarian Republic of)": "Venezuela"})
    df['country'] = df['country'].replace(
        {"The former Yugoslav republic of Macedonia": "Macedonia"})
    df['country'] = df['country'].replace(
        {"Bolivia (Plurinational State of)": "Bolivia"})
    df['country'] = df['country'].replace(
        {"Micronesia (Federated States of)": "Micronesia"})
    df['country'] = df['country'].replace(
        {"Iran (Islamic Republic of)": "Iran"})

    # Get list of countries with insufficient data. Theres 10 nations
    # from which data was only collected in 2013.
    all_countries = df.country.unique()
    insufficient_data_countries = []
    for country in all_countries:
        if df.country.value_counts()[country] < (df.year.max()-df.year.min()+1):
            insufficient_data_countries.append(country)

    # Filter out countries with insufficient data from df
    df = df[~df['country'].isin(insufficient_data_countries)]
    
    # Remove bmi feature
    df = df.drop(['bmi'], axis=1)

    # Interpolate missing values by country, then by year
    df = interpolate_df(df, 'country')
    df = interpolate_df(df, 'year')
    df = df.sort_values(by=['country', 'year'], ascending=[True, False])

    # Remove outliers of the percentage_expenditure column
    df['percentage_expenditure'] = mstats.winsorize(
        df['percentage_expenditure'], limits=0.25)
    df['hepatitis_b'] = mstats.winsorize(
        df['hepatitis_b'], limits=0.15)

    return df

