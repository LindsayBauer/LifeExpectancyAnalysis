import numpy as np
import sklearn.metrics
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

from analysis import LAST_YEAR
from heatmap import (get_df_with_binary_status, get_features,
                               get_weak_corr_features)

df = get_df_with_binary_status()
NUMERIC_FEATURES = get_features()
WEAK_CORR_FEATURES = get_weak_corr_features()
COLLINEAR_FEATURES = ['adult_mortality', 'under-five_deaths', 'polio', 'diphtheria', 'thinness_10-19_years',
                      'thinness_5-9_years', 'income_composition_of_resources', 'Developing']


def drop_features(df):
    ''' Remove weakly correlated and collinear feature columns from specified df. '''
    features_to_remove = COLLINEAR_FEATURES + WEAK_CORR_FEATURES
    df = df.drop([feat for feat in features_to_remove], axis=1)
    return df


def get_model_data():
    ''' Return data to train multiple linear regression model. '''
    model_data = df[df.year.ne(
        LAST_YEAR)][NUMERIC_FEATURES]  # Data up to MOST_RECENT_YEAR
    return drop_features(model_data)


def get_test_data():
    ''' Return data to evaluate. '''
    test_data = df[df.year.eq(
        LAST_YEAR)][NUMERIC_FEATURES]  # Data from MOST_RECENT_YEAR
    return drop_features(test_data)


def get_model_stats():
    ''' Print model parameters (Intercept and Coefficients) and measures of predictive
    strength (R², RSE, RMSE, MAE) obtained via multiple linear regression. '''
    # Actual life expectancies from MOST_RECENT_YEAR
    test_life_expectancies = list(get_test_data().life_expectancy)
    # Data to use to predict life expectancies in MOST_RECENT_YEAR
    data_for_LE_prediction = get_test_data().drop(
        ['life_expectancy'], axis=1).to_numpy()

    # Multiple linear regression via SciKit Learn
    model = LinearRegression()
    X = get_model_data().drop(['life_expectancy'], axis=1)
    Y = get_model_data().life_expectancy
    model.fit(X, Y)
    print(f"Intercept: {model.intercept_}")
    print(f"Coefficients: {model.coef_}")
    print(f"R²: {model.score(X, Y)}")

    # Make predictions for LE's of countries in 2015 and calculate error against their actual known LE's
    predictions = np.zeros(len(test_life_expectancies))
    for i in range(len(test_life_expectancies)):
        LE_prediction = model.predict([list(data_for_LE_prediction[i])]).item()
        predictions[i] = LE_prediction

    print(
        f"Mean Squared Error (RSE): {sklearn.metrics.mean_squared_error(test_life_expectancies, predictions)}")
    print(
        f"Root Mean Squared Error (RMSE): {np.sqrt(sklearn.metrics.mean_squared_error(test_life_expectancies, predictions))}")
    print(
        f"Mean Absolute Error: {sklearn.metrics.mean_absolute_error(test_life_expectancies, predictions)}")


def get_OLS_summary():
    ''' Print model's Ordinary Least Squares Regression Results. '''
    # Multiple linear regression via StatsModels
    X = get_model_data().drop(['life_expectancy'], axis=1)
    X = sm.add_constant(X)  # Add intercept manually
    model = sm.OLS(get_model_data().life_expectancy, X).fit()
    print(model.summary())


if __name__ == '__main__':
    get_model_stats()
    get_OLS_summary()
