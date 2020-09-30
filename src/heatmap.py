import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis import Color
from get_data import SRC_DIR, get_df

THRESHOLD = 0.5


def get_df_with_binary_status():
    ''' Replace 'status' feature column in df with a 'Developed' column and a 'Developing' column. If 
    a country is 'Developed' there will be 1's in the 'Developed' column and 0's in the 'Developing' 
    column. Vise versa for a 'Developing' country. Return the df. '''
    df = get_df()

    # Convert categorial 'status' column into two dummy value columns: 'Developed' and 'Developing'
    binary_status = pd.get_dummies(df.status)
    df_with_binary_status = df.drop(columns='status').join(binary_status)
    return df_with_binary_status


def get_features():
    ''' Return a list of all numeric features in the data frame '''
    df = get_df_with_binary_status()
    return(list(df.columns)[2:])


def get_weak_corr_features():
    ''' Return a list of features with correlations to life expectancy
     in range (-THRESHOLD, THRESHOLD). '''
    features = get_features()
    correlations = get_df_with_binary_status(
    )[features].corr()  # Correlation Matrix
    # Correlations of each feature to life expectancy
    LE_correlations = correlations.iloc[0, :]
    i = 0
    weak_corr_features = []
    for row in LE_correlations:
        if abs(round(row, 2)) <= THRESHOLD:
            weak_corr_features.append(features[i])
        i += 1
    return weak_corr_features


def plot_heatmap():
    ''' Plots heatmap showing the correlation of all data features to LE, including
    status types (Developed and Developing). '''
    # Generate correlation matrix
    correlations = get_df_with_binary_status().iloc[:, 2:].corr()
    # Retain heatmap below main diagonal
    mask = np.triu(correlations, k=0)

    # Generate heatmap
    plt.figure(figsize=(16, 8))
    sns.heatmap(correlations, annot=True, fmt='.2g', vmin=-1,
                vmax=1, center=0, cmap='coolwarm', mask=mask)
    plt.title("Features Correlation Heatmap",
              color=Color.GREY.value, weight='bold', fontsize=15)
    plt.tight_layout()
    plt.savefig(SRC_DIR / "graphs" / "heatmap.png")


if __name__ == '__main__':
    plot_heatmap()
