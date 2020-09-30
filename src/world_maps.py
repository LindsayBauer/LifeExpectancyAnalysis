import plotly.graph_objects as go

from analysis import LAST_YEAR, check_year_validity
from get_data import SRC_DIR, get_df

df = get_df()

MIN_LE = df['life_expectancy'].min()
MAX_LE = df['life_expectancy'].max()

MIN_EXP = df['total_expenditure'].min()
MAX_EXP = df['total_expenditure'].max()


def plot_worldmap_LE(year=LAST_YEAR):
    ''' Plot the life expectency of each country on a world map. '''
    year = check_year_validity(year)
    df_by_year = df[df.year.eq(year)]

    worldmap = [dict(type='choropleth', locations=df_by_year['country'], locationmode='country names',
                     z=df_by_year['life_expectancy'], zmin=MIN_LE, zmax=MAX_LE, colorscale="Blues", reversescale=False,
                     marker=dict(line=dict(width=0.5)),
                     colorbar=dict(title='Life Expectancy (Years)'))]

    layout = dict(title=str(year) + ' Global Life Expectancy', geo=dict(showframe=False,
                                                                        showcoastlines=False, projection=dict(type='equirectangular')))

    fig = go.Figure(data=worldmap, layout=layout)
    fig.show()


def plot_worldmap_spending(year=LAST_YEAR):
    ''' Plot % of government expenditure on health on a world map. '''
    year = check_year_validity(year)
    df_by_year = df[df.year.eq(year)]

    worldmap = [dict(type='choropleth', locations=df_by_year['country'], locationmode='country names',
                     z=df_by_year['total_expenditure'], zmin=MIN_EXP, zmax=MAX_EXP, colorscale="Blues", reversescale=False,
                     marker=dict(line=dict(width=0.5)),
                     colorbar=dict(title='Government Expenditure on Health (%)'))]

    layout = dict(title='Government Expenditure on Health as a % of Total Expenditure in ' + str(year),
                  geo=dict(showframe=False, showcoastlines=False, projection=dict(type='equirectangular')))

    fig = go.Figure(data=worldmap, layout=layout)
    fig.show()


if __name__ == '__main__':
    import sys
    try:
        year = sys.argv[1]
        plot_worldmap_LE(int(year))
        plot_worldmap_spending(int(year))
    except IndexError:
        plot_worldmap_LE()
        plot_worldmap_spending()
