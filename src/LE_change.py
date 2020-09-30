import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm

from analysis import Color, get_change_in_LE
from get_data import SRC_DIR, get_df

df = get_df()

COUNTRIES = list(df.country.unique())


def get_LE_changes():
    ''' Return a 2D array with dimmensions (number_countries,2). First column is countries in the dataset.
    Second column is the change in life expectancy experienced by the country in years spanned by the dataset. '''
    le_changes = []
    for country in COUNTRIES:
        le_changes.append([country, round(get_change_in_LE(country), 2)])

    return np.array(le_changes)


def plot_LE_changes():
    ''' Plot the change in LE of each country between years spanned by the dataset. '''
    le_changes = get_LE_changes()
    country = list(le_changes[:, 0])
    change = [float(i) for i in list(le_changes[:, 1])]

    df = pd.DataFrame({'country': country,
                       'change': change})

    # Make barplot and sort bars by height
    plt.figure(figsize=(16, 6))
    sns.barplot(x='country',
                y='change',
                data=df,
                order=df.sort_values('change').country)

    # Format axis' ticks
    plt.xticks(fontsize=6, rotation=90)
    plt.yticks(fontsize=8)

    # Format labels and title
    plt.xlabel('', size=2)
    plt.ylabel("Change in Life Expectancy", size=12, color=Color.GREY.value)
    plt.title("Change in Life Expectancy Between 2000 and 2015 By Country",
              size=16, weight='bold', color=Color.GREY.value)

    plt.tight_layout()
    plt.savefig(SRC_DIR / "graphs" / "LE_change.png")


if __name__ == '__main__':
    plot_LE_changes()
