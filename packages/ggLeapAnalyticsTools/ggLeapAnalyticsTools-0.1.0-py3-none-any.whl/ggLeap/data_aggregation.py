from datetime import datetime, date

import pandas as pd
import numpy as np

from . import helpers
from . import DataHandler


def remove_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove dates from all datetimes in a dataframe
    """

    new_records = []
    for i in range(len(df)):
        current_record = df.loc[i].copy()
        date_string = current_record["Date"]
        dt = helpers.ggLeap_str_to_datetime(date_string)
        new_dt = helpers.remove_date_datetime(dt)
        current_record["Date"] = new_dt
        new_records.append(current_record.copy())

    return pd.DataFrame(new_records)


def remove_weeks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove all weeks from datetimes

    Change all dates in the DataFrame to the following:
    DD/MM/YY
    01/01/01 for a Monday
    02/01/01 for a Tuesday
    03/01/01 for a Wednesday
    04/01/01 for a Thursday
    05/01/01 for a Friday
    06/01/01 for a Saturday
    07/01/01 for a Sunday
    """

    dates = []
    new_records = []
    for i in range(len(df)):
        current_record = df.loc[i].copy()
        date_string = current_record["Date"]
        dt = helpers.ggLeap_str_to_datetime(date_string)
        new_dt = helpers.remove_week_datetime(dt)
        current_record["Date"] = new_dt
        new_records.append(current_record.copy())

        date = date_string.split(" ")[0]
        if date not in dates:
            dates.append(date)

    days = [0 for i in range(7)]
    for date in dates:
        day = helpers.ggLeap_get_weekday_no_time(date)
        days[day] += 1

    return pd.DataFrame(new_records.copy()), days


def collect_actions(
    df: pd.DataFrame, action: str
) -> tuple[list[date], list[pd.Series]]:
    action_records = df.loc[df["Action"] == action]

    dates: list[date] = []
    action_dates_datetimes: list[list[date]] = [[]]
    for i in range(len(action_records)):
        date = action_records.iloc[i]["Date"]
        date_no_time = date.date()

        if date_no_time in dates:
            j = dates.index(date_no_time)
            action_dates_datetimes[j].append(date)
        else:
            dates.append(date_no_time)
            action_dates_datetimes.append([])

            j = dates.index(date_no_time)
            action_dates_datetimes[j].append(date)

    colns: list[pd.DataFrame] = []
    for entry in action_dates_datetimes:
        colns.append(pd.Series(entry))

    return dates, colns


def collect_logins(df: pd.DataFrame) -> tuple[list[date], list[pd.Series]]:
    normal_dates, normal_datetimes = collect_actions(df, "LoggedIn")
    external_dates, external_datetimes = collect_actions(df, "ExternalLogin")

    date_set = list(set(normal_dates + external_dates))

    new_dates = []
    datetimes = []
    for date in date_set:
        if date in normal_dates and date in external_dates:
            i, j = normal_dates.index(date), external_dates.index(date)
            datetimes.append(pd.concat([normal_datetimes[i], external_datetimes[j]]))
            new_dates.append(date)
        elif date in normal_dates and date not in external_dates:
            i = normal_dates.index(date)
            datetimes.append(normal_datetimes[i])
            new_dates.append(date)
        elif date not in normal_dates and date in external_dates:
            j = external_dates.index(date)
            datetimes.append(external_datetimes[i])
            new_dates.append(date)
        else:
            raise Exception("Something went wrong.")

    return new_dates, datetimes


def collect_logouts(df: pd.DataFrame) -> tuple[list[date], list[pd.Series]]:
    logout_dates, logout_datetimes = collect_actions(df, "LoggedOut")

    return logout_dates, logout_datetimes


def generate_cumulative_distribution(
    days: list[date], data: list[pd.Series]
) -> tuple[list, list]:

    cum_actions: list[tuple[list, list]] = []
    for i in range(len(days)):
        count: int = 1
        data[i].sort_values(ascending=True, inplace=True)

        temp_cum_actions: tuple[list, list] = ([], [])
        for action in data[i]:
            temp_cum_actions[0].append(action)
            temp_cum_actions[1].append(count)
            count += 1

        cum_actions.append(temp_cum_actions)

    return days, cum_actions


def total_user_seconds(dh: DataHandler.DataHandler, username: str) -> int:
    """
    Iterate across all of a user's logins and logouts to calculate
    the total amount of time that they've spent logged in
    """
    pass


def total_user_seconds_between(
    dh: DataHandler.DataHandler, username: str, start: int, end: int
) -> int:
    """
    Iterate across all of a user's logins and logouts to calculate
    the total amount of time that they've spent logged in between two times
    """
    pass
