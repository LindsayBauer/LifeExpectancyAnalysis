import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from analysis import Color, LAST_YEAR, check_year_validity
from get_data import SRC_DIR, get_df

df = get_df()


def get_top_spenders(number=20, year=LAST_YEAR):
    ''' Return a 2D array with dimmensions (number,2). First column lists the [number] countries that 
    spent the most on healthcare as a percentage of total government spending in [year]. Second 
    column lists the percentage. '''
    df_by_year = df[df.year.eq(year)]
    top_spenders = df_by_year.sort_values(
        by=['total_expenditure'], ascending=False).head(number)
    result_arr = top_spenders[['country', 'total_expenditure']].to_numpy()
    return result_arr


def get_LE(country, year):
    ''' Return life expectancy for specified country in specified year. '''
    data_by_year = df[df['year'].eq(year)]
    le = data_by_year[(data_by_year['country'].eq(country))
                      ]['life_expectancy'].item()
    return le


def plot_expenditure_versus_LE(number=20, year=2015):
    ''' Plot a double horizontal bar graph showing: 1) the % of total government spending
    on healthcare and 2) the life expectancy of specific countries. The countries shown
    are the [number] countries who spend the most on healthcare as a % of total government spending
    in the specified year. '''
    year = check_year_validity(year)
    top_spenders = get_top_spenders(number, year)

    # Data for plotting
    countries = top_spenders[:, 0]
    spending_percentages = top_spenders[:, 1]
    life_expectancies = []
    for country in countries:
        life_expectancies.append(get_LE(country, year))

    # Sort countries and their LE via health care spending % (descending)
    idx = spending_percentages.argsort()
    countries, spending_percentages, life_expectancies = [
        np.take(x, idx) for x in [countries, spending_percentages, life_expectancies]]

    y = np.arange(life_expectancies.size)

    # Plot the two bar graphs side-by-side
    fig, axes = plt.subplots(ncols=2, sharey=True)
    axes[0].barh(y, spending_percentages, align='center',
                 color=[Color.DARK_BLUE.value, Color.LIGHT_BLUE.value], zorder=10)
    axes[0].set_title(str(year) + ' Government Healthcare Spending as % of Total',
                      fontsize=10, weight='bold', color=Color.GREY.value)
    axes[1].barh(y, life_expectancies, align='center',
                 color=[Color.DARK_BLUE.value, Color.LIGHT_BLUE.value], zorder=10)
    axes[1].set_title(str(year) + ' Life Expectancy (years)',
                      fontsize=10, weight='bold', color=Color.GREY.value)

    # Have values of left sub_plot's x-axis increase from right to left
    axes[0].invert_xaxis()

    # Center y-axis labels between 2 subplots
    axes[0].set(yticks=y, yticklabels=[])
    for yloc, state in zip(y, countries):
        axes[0].annotate(state, (0.5, yloc), xycoords=('figure fraction', 'data'),
                         ha='center', va='center')
    axes[0].yaxis.tick_right()

    for ax in axes.flat:
        ax.margins(0.02)
        ax.grid(True)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.6)  # Increase space between the two bar plots
    plt.savefig(SRC_DIR / "graphs" / "hc_spending_vs_LE.png")

if __name__ == '__main__':
    plot_expenditure_versus_LE()
