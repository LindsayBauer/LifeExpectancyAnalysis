import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Patch

from analysis import LAST_YEAR, Color
from get_data import SRC_DIR, get_df

df = get_df()

COUNTRIES = list(df.country.unique())


def get_recent_data_sorted():
    ''' Return DataFrame of data from most recent year sorted in order of ascending LE. '''
    df_by_year = df[df['year'].eq(LAST_YEAR)]
    ascending_LE_df = df_by_year.sort_values(
        by=['life_expectancy'], ascending=True)

    return ascending_LE_df


def plot_LE_by_status():
    ''' Plot a bar graph showing the LE of countries in ascending order, colored by country status. '''
    ascending_LE_df = get_recent_data_sorted()
    statuses = list(ascending_LE_df['status'])
    status_colors = [Color.LIGHT_BLUE.value, Color.ORANGE.value]
    colors = []
    for status in statuses:
        if status == "Developing":
            colors.append(status_colors[0])
        else:
            colors.append(status_colors[1])
    ascending_LE_df['color'] = colors

    # Create custom legend
    legend_elements = [Patch(facecolor=status_colors[0], label='Developing'),
                       Patch(facecolor=status_colors[1], label='Developed')]

    # Plot bar graph
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.bar(ascending_LE_df['country'],
           ascending_LE_df['life_expectancy'], color=ascending_LE_df['color'])
    
    # Format axis
    plt.xticks(ascending_LE_df['country'], fontsize=6, rotation=90)
    ax.legend(handles=legend_elements, loc='upper left')
    plt.xlim([-1, len(ascending_LE_df['country'])])

    # Set labels and titles 
    plt.ylabel("Life Expectancy (years)", size=12)
    plt.title("2015 Life Expectancy By Country",
              size=16, weight='bold', color=Color.GREY.value)

    plt.tight_layout()
    plt.savefig(SRC_DIR / "graphs" / "LE_by_status.png")

if __name__ == '__main__':
    plot_LE_by_status()
