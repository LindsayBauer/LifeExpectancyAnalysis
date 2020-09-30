import matplotlib.pyplot as plt
import seaborn as sns

from analysis import FIRST_YEAR, LAST_YEAR, Color
from get_data import SRC_DIR, get_df

df = get_df()


def plot_LE_distribution():
    ''' Plot overlapping histograms of LE for first and last spanned by data. '''
    sns.distplot(df[df.year.eq(FIRST_YEAR)]["life_expectancy"],
                 color=Color.ORANGE.value, label=str(FIRST_YEAR))
    sns.distplot(df[df.year.eq(LAST_YEAR)]["life_expectancy"],
                 color=Color.LIGHT_BLUE.value, label=str(LAST_YEAR))
    plt.legend()
    plt.xlabel("Life Expectancy (years)", color=Color.GREY.value)
    plt.ylabel("Number of Countries", color=Color.GREY.value)
    plt.title("Life Expectancy Distribution",
              fontsize=14, weight='bold', color=Color.GREY.value)
    plt.tight_layout()
    plt.savefig(SRC_DIR / "graphs" / "LE_histogram.png")

if __name__ == '__main__':
    plot_LE_distribution()
