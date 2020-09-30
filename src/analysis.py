from enum import Enum

from get_data import SRC_DIR, get_df

df = get_df()

FIRST_YEAR, LAST_YEAR = df['year'].min(), df['year'].max()
COUNTRIES = df.country.unique()

# HEX codes of colors used throughout graphs
class Color(Enum):
    LIGHT_BLUE = '#43B7C2'
    DARK_BLUE = '#164B79'
    ORANGE = '#F58624'
    GREY = '#4f5666'
    YELLOW = '#D4C44E'
    GREEN = '#B5D63D'
    TEAL = '#29848F'


def check_year_validity(year):
    ''' Check that the year provided is covered by the dataset. If not,
    set the year to the most recent year that data was collected. '''
    if (year > LAST_YEAR or year < FIRST_YEAR):
        year = LAST_YEAR
    return year


def get_change_in_LE(country):
    ''' Return the change in life expectancy (LE) of given country
    over the years spanned by the dataset. '''
    initial_LE = float(df[df.country.eq(country) & df.year.eq(FIRST_YEAR)]
                       ['life_expectancy'])
    final_LE = float(df[df.country.eq(country) & df.year.eq(LAST_YEAR)]
                     ['life_expectancy'])
    return final_LE - initial_LE


def get_largest_LE_increase():
    ''' Return string stating the country with the largest increase in life expectancy (LE)
    over the years spanned by the dataset, and the LE itself. '''
    biggest_LE_increase = 0
    nation = ''  # Nation with the biggest increase in LE

    for country in COUNTRIES:
        LE_change = get_change_in_LE(country)
        if LE_change > biggest_LE_increase:
            biggest_LE_increase = round(LE_change, 1)
            nation = country

    return (f"{nation} experienced the largest increase in life expectancy between "
            f"{FIRST_YEAR} and {LAST_YEAR}: {biggest_LE_increase} years")


def get_countries_with_decreased_LE():
    ''' Return list of countries where LE decreased over years spanned by the dataset. '''
    experienced_LE_decrease = []

    for country in COUNTRIES:
        LE_change = get_change_in_LE(country)
        if LE_change < 0:
            experienced_LE_decrease.append(country)

    return experienced_LE_decrease


def countries_with_decreased_LE_string():
    ''' Return string stating countries whose LE decreased over years spanned by dataset. '''
    experienced_LE_decrease = get_countries_with_decreased_LE()
    countries = ", ".join(experienced_LE_decrease)

    return ("The countries that experienced a decrease in life expectancy between "
            f"{FIRST_YEAR} and {LAST_YEAR}: {countries} ")


def get_lowest_LE_country(year=LAST_YEAR):
    ''' Return country (or countries) with the lowest LE for given year, and the LE itself. '''
    year = check_year_validity(year)
    data_of_year = df[df.year.eq(year)]
    lowest_LE = data_of_year['life_expectancy'].min()
    lowest_LE_countries = list(data_of_year[data_of_year['life_expectancy'].eq(
        lowest_LE)]['country'])

    return lowest_LE_countries, lowest_LE


def lowest_LE_country_string(year=LAST_YEAR):
    ''' Return string stating the country (or countries) with the lowest LE for 
    given year, and the LE itself. '''
    lowest_LE_countries, lowest_LE = get_lowest_LE_country(year)
    countries_string = ", ".join(lowest_LE_countries)

    return (f"{countries_string} had the lowest life expectancy of any country in "
            f"{year}: {lowest_LE} years")


def get_highest_LE_country(year=LAST_YEAR):
    ''' Return country (or countries) with the highest LE for given year, 
    and the LE itself. '''
    year = check_year_validity(year)
    data_of_year = df[df.year.eq(year)]
    highest_LE = data_of_year['life_expectancy'].max()
    highest_LE_countries = list(data_of_year[data_of_year['life_expectancy'].eq(
        highest_LE)]['country'])

    return highest_LE_countries, highest_LE


def highest_LE_country_string(year=LAST_YEAR):
    ''' Return string stating the country (or countries) with the highest 
    LE for given year, and the LE itself. '''
    highest_LE_countries, highest_LE = get_highest_LE_country(year)
    countries_string = ", ".join(highest_LE_countries)

    return (f"{countries_string} had the highest life expectancy of any country in "
            f"{year}: {highest_LE} years")


def get_lowest_developed_LE(year=LAST_YEAR):
    ''' Return string stating the 'developed' country with the lowest LE for given 
    year, and the LE itself. '''
    year = check_year_validity(year)
    data_of_year = df[df.year.eq(year)]
    developed_countries_data = data_of_year[data_of_year['status'].eq(
        'Developed')]
    lowest_developed_LE = developed_countries_data['life_expectancy'].min()
    nation = developed_countries_data[developed_countries_data['life_expectancy'].eq(
        lowest_developed_LE)]['country'].item()

    return (f"{nation} was the 'developed' country with the lowest life expectancy in "
            f"{year}: {lowest_developed_LE} years")


def get_num_high_developing_LE():
    ''' Return string stating the number of 'developing' countries with LE higher than or equal to
    the LE of at least one 'developed' country in the most recent year. '''
    most_recent_data = df[df.year.eq(LAST_YEAR)]
    developed_countries_data = most_recent_data[most_recent_data['status'].eq(
        'Developed')]
    developing_countries_data = most_recent_data[most_recent_data['status'].eq(
        'Developing')]
    lowest_developed_LE = developed_countries_data['life_expectancy'].min()
    higher_than_developed = developing_countries_data[developing_countries_data['life_expectancy'].ge(
        lowest_developed_LE)]
    nations = higher_than_developed.country.unique()

    return ("Number of 'developing' countries with life expectancies ≥ one or more 'developed' countries in "
            f"{LAST_YEAR}: {len(nations)}")


if __name__ == '__main__':
    md_bullet = '- '
    single_space = '\n'
    double_space = '\n'*2

    with open((SRC_DIR / "Global_Life_Expectancy_Analysis.md"), 'w+') as file:
        file.seek(0)
        file.write("## Exploratory Data Analysis:" + double_space)

        file.write("### Change Across Years:" + single_space)
        file.write(md_bullet + get_largest_LE_increase() + double_space)
        file.write(md_bullet + countries_with_decreased_LE_string() + double_space)
 
        file.write("### Most Recent Year:" + single_space)
        file.write(md_bullet + lowest_LE_country_string() + double_space)
        file.write(md_bullet + highest_LE_country_string() + double_space)
        file.write(md_bullet + get_lowest_developed_LE() + double_space)
        file.write(md_bullet + get_num_high_developing_LE() + double_space)
