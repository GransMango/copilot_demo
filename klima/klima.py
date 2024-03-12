import pandas as pd
import pathlib
import altair as alt
import re

def get_realtemp(row : pd.Series, df_mean : pd.DataFrame) -> float:
    """
    A function to add the anomaly to the average temperature for rows month.
    This was the easiest way I found to do it.

    Args:
        row (pd.Series): the row being passed in the select function
        df_mean (pd.DataFrame): A dataframe containing average temperature

    Returns:
        float: representing the current month temperature

    """
    return round(df_mean.at[row.name%12, "land & sea"] + row["anomaly"], 2)

def temp_to_df(file_directory: pathlib.Path | str) -> pd.DataFrame:
    """
    A function that takes in your file_directory containing the clima_history.csv and clima_mean.csv
    Args:
        file_directory (pathlib.Path or str) : The directory of your clima files

    Returns:
        pd.DataFrame: Dataframe containing the temperatures for each month.

    """

    current_dir = file_directory.as_posix()
    df_history = pd.read_csv(current_dir + "/clima_history.csv")
    df_mean = pd.read_csv(current_dir + "/clima_mean.csv")

    # Remove chars from number https://stackoverflow.com/questions/13682044/remove-unwanted-parts-from-strings-in-a-column
    df_mean["land & sea"] = df_mean["land & sea"].map(lambda x: re.sub(r'[^0-9.-]', '', x)).astype(float)

    df_history["month"] = df_history["year"].astype(str).str[-2:].astype(int)
    df_history["year"] = df_history["year"].astype(str).str[:4].astype(int)

    df_history["anomaly"] = df_history.apply(get_realtemp, axis=1, args=(df_mean,))
    df_history = df_history.rename(columns={"anomaly": "temp"})

    return df_history

def get_chart() -> dict:
    """
    A function that gets the chart representing the clima temperatures. 
    Done by creating 2 charts and then layering them
    Returns:
        dict: Returns a dict object containing chart.
    """
    df_history = temp_to_df(pathlib.Path.cwd())
    df_2022 = df_history.tail(12)
    chart = alt.Chart(df_history).mark_line(color="blue", opacity=0.02).encode(
        alt.Size("year"),
        x="month:Q",
        y="temp:Q",
    )

    chart_2022 = alt.Chart(df_2022).mark_line(interpolate="monotone").encode(
        alt.Size("year"),
        x="month:Q",
        y="temp:Q",
        color="year:N",
        tooltip=[alt.Tooltip('month:Q'),
                 alt.Tooltip('year:Q'),
                 alt.Tooltip('temp:N'),
                 alt.Tooltip()
                 ]
    )

    return alt.layer(chart, chart_2022)
