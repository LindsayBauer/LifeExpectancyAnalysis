import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from analysis import FIRST_YEAR, LAST_YEAR, Color, get_countries_with_decreased_LE
from get_data import SRC_DIR, get_df

df = get_df()

IMMUNIZATIONS = ['hepatitis_b', 'polio', 'diphtheria']
THINNESS = ['thinness_5-9_years', 'thinness_10-19_years']
EARLY_MORTALITY = ['under-five_deaths', 'infant_deaths']
DECREASED_LE = get_countries_with_decreased_LE()
PALETTE = [Color.LIGHT_BLUE.value, Color.DARK_BLUE.value,
           Color.ORANGE.value]  # Colors for line graph


def plot_decreasing_LE_trend(trend, title, file_name, lower_limit=0, upper_limit=400):
    ''' Plot a grid of side-by-side line graphs showing specified trend for the countries
    whose LE decreased over the years spanned by the data. '''
    # Extract relevant DataFrame columns
    filtered_data = df[['country', 'year']+trend]

    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(10, 8))

    num = 0  # Index of subplot
    for country in DECREASED_LE:
        # Isolate relevant DataFrame rows
        country_data = filtered_data[filtered_data.country.eq(
            country)].sort_values(by='year', ascending=True)
        num += 1

        # Specify correct location on plot
        plt.subplot(3, 3, num)

        # Plot immunization trend lines
        for i in range(len(trend)):
            plt.plot(range(FIRST_YEAR, LAST_YEAR+1),
                     country_data[trend[i]], marker='', color=PALETTE[i], linewidth=1.9, label=country)

        # Same y-axis limits for all subplots
        plt.ylim(lower_limit, upper_limit)

        plt.title(country, loc='left', fontsize=12,
                  weight='bold', color=Color.GREY.value)

    # Create legend
    legend_elements = []
    for i in range(len(trend)):
        legend_elements.append(
            Patch(facecolor=PALETTE[i], label=trend[i].replace('_', ' ').title()))

    plt.figlegend(handles=legend_elements, loc='lower center',
                  ncol=3, fancybox=True, bbox_to_anchor=(0.5, .05))
    plt.suptitle(f"{title}, 2000-2015",
                 fontsize=15, weight='bold', color=Color.GREY.value, y=.94)

    image_name = "decreasing_LE_" + file_name + ".png"
    plt.savefig(SRC_DIR / "graphs" / image_name)


def plot_trends():
    plot_decreasing_LE_trend(
        IMMUNIZATIONS, "Immunization Rate of 1 Year Olds", "immunizations", 20, 110)
    plot_decreasing_LE_trend(THINNESS, "Rate of Thinness", "thinness", 0, 15)
    plot_decreasing_LE_trend(
        EARLY_MORTALITY, "Mortality per 1000 Population", "mortality")


if __name__ == '__main__':
    plot_trends()
