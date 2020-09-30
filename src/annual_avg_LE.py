import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from analysis import FIRST_YEAR, LAST_YEAR, Color
from get_data import SRC_DIR, get_df

df = get_df()


def get_LE_statistics(years, statuses):
    ''' Return two matrices: First is annual average of LE (row) by status (column). The
    second is annual standard deviations of LE (columns) by status (rows). '''
    annual_LE_avg_by_status = np.zeros(shape=(len(years), len(statuses)))
    annual_LE_std_by_status = np.zeros(shape=(len(statuses), len(years)))

    for i in range(len(statuses)):
        # For each status get LE avg and std by year
        for year in years:
            # Filter df by status and year
            annual_data = df[df.status.eq(statuses[i]) & df.year.eq(year)]
            avg = annual_data['life_expectancy'].mean()
            std = annual_data['life_expectancy'].std()
            annual_LE_avg_by_status[years.index(
                year)][i] = round(avg, 1)
            annual_LE_std_by_status[i][years.index(year)] = round(std, 1)

    return annual_LE_avg_by_status, annual_LE_std_by_status


def plot_annual_average_LE():
    ''' Plot a double bar graph of annual average LE by status with error bars. '''
    years = [year for year in range(FIRST_YEAR, LAST_YEAR+1)]
    statuses = df.status.unique()
    colors = [Color.LIGHT_BLUE.value, Color.DARK_BLUE.value]

    annual_LE_averages, annual_LE_std = get_LE_statistics(years, statuses)

    # Plot and style bar graph
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    df_ages_by_year = pd.DataFrame(annual_LE_averages, index=years)
    df_ages_by_year.plot.bar(legend=True, yerr=annual_LE_std, ecolor=Color.ORANGE.value, figsize=(
        14, 6), color=colors, rot=0)
    plt.ylim(40,)  # Set lower limit to y-axis
    plt.legend(statuses, loc='upper left')

    # Format labels
    plt.xlabel("Year", fontsize=14, color=Color.GREY.value)
    plt.ylabel("Life Expectancy (Years)", fontsize=14, color=Color.GREY.value)
    plt.title("Average Life Expectancy",
              fontsize=17, color=Color.GREY.value, weight='bold')
    plt.tight_layout()
    plt.savefig(SRC_DIR / 'graphs' / 'annual_avg_LE.png')



if __name__ == '__main__':
    plot_annual_average_LE()
