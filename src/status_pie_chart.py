import matplotlib.pyplot as plt

from analysis import LAST_YEAR, Color
from get_data import SRC_DIR, get_df

df = get_df()

def plot_status_pie_chart():
    ''' Plot a pie chart of the proportion of 'Developed' v 'Developing' countries in most recent year. '''
    num_developed_countries = len(
        df[(df['status'].eq('Developed')) & (df['year'].eq(LAST_YEAR))])
    num_developing_countries = len(
        df[(df['status'].eq('Developing')) & (df['year'].eq(LAST_YEAR))])

    labels = ['Developed', 'Developing']
    sizes = [num_developed_countries, num_developing_countries]
    explode = (0.05, 0)  # How much to detach slice from rest of pie
    colors = [Color.LIGHT_BLUE.value, Color.DARK_BLUE.value]

    # Generate the pie chart
    fig1, ax1 = plt.subplots(figsize=(4,4))
    _, texts, autopcts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                                 shadow=False, startangle=5)
    # Format labels and percentages
    plt.setp(texts, **{'color': Color.GREY.value, 'fontsize': 13})
    plt.setp(autopcts, **{'color': 'w', 'weight': 'bold', 'fontsize': 13})
    ax1.set_title("Country Statuses, 2015", fontdict={
                  'fontsize': 20, 'weight': 'bold'}, color=Color.GREY.value)
    plt.tight_layout()
    plt.savefig(SRC_DIR / "graphs" / "status_pie_chart.png")

if __name__ == '__main__':
    plot_status_pie_chart()
