import matplotlib.pyplot as plt
import numpy as np

from analysis import Color, get_highest_LE_country, get_lowest_LE_country
from get_data import SRC_DIR, get_df

df = get_df()

YEARS = list(df.year.unique())


def get_longest_LE_countries():
    ''' Return a list of the countries with the longest life expectancy by year. '''
    countries = []
    for year in YEARS:
        nations, _ = get_highest_LE_country(year)
        nation_list = ", ".join(nations)
        countries.append(nation_list)
    return countries


def get_shortest_LE_countries():
    ''' Return a list of the countries with the shortest life expectancy by year. '''
    countries = []
    for year in YEARS:
        nations, _ = get_lowest_LE_country(year)
        nation_list = ", ".join(nations)
        countries.append(nation_list)
    return countries


def plot_timeline(countries, title, file):
    ''' Plot the specified countries on a timeline with the given title and save it to the given file. '''
    levels = np.tile([-5, 5, -3, 3, -1, 1],
                     int(np.ceil(len(YEARS)/6)))[:len(YEARS)]

    # Create figure
    fig, ax = plt.subplots(figsize=(18, 6), constrained_layout=True)
    plt.title(title, weight='bold', color=Color.GREY.value, fontsize=20)

    # Plot stem plot; place vertical lines at each year from baseline to vertical levels
    markerline, stemline, baseline = ax.stem(YEARS, levels,
                                             linefmt="C0-", basefmt="C9-",
                                             use_line_collection=True)

    # Format markers
    plt.setp(markerline, mec=Color.ORANGE.value, mfc=Color.ORANGE.value, zorder=3)

    # Shift markers to the baseline by replacing y-data with zeros
    markerline.set_ydata(np.zeros(len(YEARS)))

    # Annotate stem lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for yr, l, c, v in zip(YEARS, levels, countries, vert):
        ax.annotate(c, xy=(yr, l), xytext=(-3, np.sign(l)*3),
                    textcoords="offset points", va=v, ha="right", fontsize=12)

    # Format year tick labels 
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # Remove y-axis and lines denoting data area boundaries (spines)
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    # Set padding between stemlines and x-axis
    ax.margins(y=0.1)
    plt.savefig(SRC_DIR / "graphs" / (file + "_LE_timeline.png"))


def plot_longest_LE_timeline():
    ''' Plot a timeline showing the countries with the longest LE by year '''
    countries = get_longest_LE_countries()

    plot_timeline(
        countries, "Countries with Longest Life Expectancies", "longest")


def plot_shortest_LE_timeline():
    ''' Plot a timeline showing the countries with the shortest LE by year '''
    countries = get_shortest_LE_countries()

    plot_timeline(
        countries, "Countries with Shortest Life Expectancies", "shortest")


if __name__ == '__main__':
    plot_longest_LE_timeline()
    #plot_shortest_LE_timeline()
