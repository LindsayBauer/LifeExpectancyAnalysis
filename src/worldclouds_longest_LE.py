import random

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from analysis import FIRST_YEAR, LAST_YEAR, Color
from get_data import SRC_DIR, get_df

df = get_df()

years_of_interest = [FIRST_YEAR, LAST_YEAR]


def get_top_LE_countries(year):
    ''' Return dictionary of the 10 countries with the highest life expectancies. '''
    df_by_year = df[df.year.eq(year)]
    LE_proportions = {}
    top_LE_countries = df_by_year.sort_values(
        by=['life_expectancy'], ascending=False).head(10)
    total = top_LE_countries['life_expectancy'].sum()
    for row in top_LE_countries.itertuples():
        LE_proportions[row[1]] = round(row[4] / total, 10)
    return LE_proportions


def color_func(**kwargs):
    ''' Generate complementary colors for words in word cloud. '''
    image_colors = [185, 208, 73]
    rand = random.randint(0, 100)
    if rand <= 35:
        col = image_colors[0]
    elif rand <= 65:
        col = image_colors[1]
    else:
        col = image_colors[2]
    rand_shade = random.randint(60, 95)
    return "hsl(" + str(col) + "," + str(rand_shade) + "%%, %d%%)" % random.randint(20, 55)


def plot_LE_wordclouds():
    ''' Plot two word clouds side-by-side of the ten countries with the highest life expectancies: one for 
    the first year in which data was collected, and the second for the last year in which data was collected. '''
    plt.figure(figsize=(10, 4))
    for i in range(len(years_of_interest)):
        LE_proportions = get_top_LE_countries(years_of_interest[i])
        wc = WordCloud(background_color="white",
                       relative_scaling=0.5).generate_from_frequencies(LE_proportions)
        plt.subplot(1, 2, 1+i)
        plt.imshow(wc.recolor(color_func=color_func, random_state=3),
                   interpolation="bilinear")
        plt.axis("off")
        plt.title("10 Longest Life Expectancies: " +
                  str(years_of_interest[i]), pad=10, color=Color.GREY.value, fontsize=13)
    plt.savefig(SRC_DIR / "graphs" / "wordclouds.png")


if __name__ == '__main__':
    plot_LE_wordclouds()
