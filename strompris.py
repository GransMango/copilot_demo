#!/usr/bin/env python3
"""
Fetches data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
import json
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """
    Fetch one day of data for one location from hvakosterstrommen.no API

    Args:
        date (datetime.date): The date you want fetched
        location (str): The location you want fetched

    Returns: Dataframe containing values.

    """
    if not date:
        date = datetime.date.today()
    datestr = date.strftime("%Y/%m-%d")
    url = "https://www.hvakosterstrommen.no/api/v1/prices/" + datestr + "_" + location + ".json"
    r = requests.get(url).content
    data = json.loads(r)
    df = pd.json_normalize(data)
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")
    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"
}
# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """
    Fetch prices for multiple days and locations into a single DataFrame

    Args:
        end_date (datetime.date): Last date you want fetched
        days (int): Amount of days before last day you want fetched
        locations list[str]: What locations you want to fetch prices for

    Returns:
        pd.DateFrame: a dataframe containing all prices.

    """

    if not end_date:
        end_date = datetime.date.today()

    dfs = []
    for i in range(days):
        for location in locations:
            date = end_date - datetime.timedelta(days=i)
            df = fetch_day_prices(date, location)
            df = df.assign(location_code=location, location=LOCATION_CODES[location])
            dfs.append(df)

    df = pd.concat(dfs)
    return df

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """
    Plot energy prices over time
    I figured some of the lines overlap and therefore seem to not appear

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Args:
        df (pd.DataFrame): Pandas DataFrame object containing prices

    Returns:
        alt.Chart: Returns an chart which contains the plot.

    """
    chart = alt.Chart(df).mark_line().encode(x="time_start:T", y="NOK_per_kWh:Q", color="location:N")
    return chart



# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """


# Task 5.6

ACTIVITIES = {
    "shower": 30,
    "baking": 2.5,
    "heat": 1
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10,
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.


    Args:
        df (pd.DataFrame): dataframe containing the prices for the day
        activity (str): chosen activity to measure price
        minutes (float): amount of time

    Returns:
        alt.Chart: chart that contains the activity plot
    """
    df["NOK_per_kWh"] = df["NOK_per_kWh"].apply(lambda x: x*(minutes/60)*ACTIVITIES[activity])
    df.rename(columns={"NOK_per_kWh": activity + " price"}, inplace=True)
    chart = alt.Chart(df).mark_line().encode(x="time_start:T", y=activity + " price:Q", color="location:N")
    return chart


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
