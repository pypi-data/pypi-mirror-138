# Nice to have:
#               - Fill missing dates
import pandas
import datetime
import random
from numpy import nan
from typing import List, Union
import csv


# -------------------------------------------------------------------------------------------------------------------
# Private methods
# -------------------------------------------------------------------------------------------------------------------
# Converts string format to datetime format
# expects string 'date' to be in format 'yyyy$mm&dd$hh$mm$ss' where $-characters do not matter
def __convert_str_to_datetime(date: str) -> datetime.datetime:
    convert_to_time_stamp(date)
    return datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]),
                             int(date[17:19]))


# Converts datetime format to string format (yyyy-mm-dd hh:mm:ss)
def __convert_datetime_to_str(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------------------------------------------------------------------------------------------
# Public methods
# -------------------------------------------------------------------------------------------------------------------

# Function:         Imports time-series via .zrx or .csv file
# Note:             Skips lines starting with '#'
# Meaning input:    file_name is the location of the data-file, ether .csv or .zrx
# Meaning output:   [pandas.Series] or pandas.Series (in case of one data set)
def import_time_series(file_name: str):
    if len(file_name) > 4:
        if file_name[-4:] == ".zrx":
            with open(file_name, "r") as tf:
                lines = tf.read().split('\n')
            c = 0
            while c < len(lines):
                if len(lines[c]) == 0:
                    del lines[c]
                    continue
                c += 1
            data = []
            c = 0
            while c < len(lines):
                data.append([])
                while lines[c][0] == "#":
                    c += 1
                while lines[c][0] != "#":
                    data[-1].append(lines[c])
                    c += 1
                    if c >= len(lines):
                        break
            data_ret = []
            for pack in data:
                times = [i.split(" ")[0] for i in pack]
                times = [convert_to_time_stamp(i) for i in times]
                values = [float(i.split(" ")[1]) for i in pack]
                data_ret.append(pandas.Series(values, times))
            if len(data_ret) == 1:
                return data_ret[0]
            return data_ret
        else:
            print("File-format is not supported")


# Function:         Exports time-series as .csv file
# Note:             -
# Meaning input:    file_name is the location of the data-file
# Meaning output:   None
def export_time_series(time_series: pandas.Series, file_name: str):
    data = [time_series.values, time_series.index]
    name = file_name + ".csv"
    data[1] = [d[0:4] + d[5:7] + d[8:10] + d[11:13] + d[14:16] + d[17:19] for d in data[1]]
    f_data = [data[1][i] + " " + ("%.2f" % data[0][i]) for i in range(len(data[0]))]
    with open(name, 'w') as csvfile:
        results_file = csv.writer(csvfile, delimiter=' ', quotechar=' ')
        for k in f_data:
            results_file.writerow(k)


# Function:         Converts String to TimeStamp String
# Note:             -
# Example input:    20211213200101          2021-12-13 20:01:01
# Example output:   2021-12-13 20:01:01     2021-12-13 20:01:01
def convert_to_time_stamp(date: str) -> str:
    if date.count("-") == 2 and len(date) == 19:
        date_split = date.split("-")
        if date_split[2].count(":") == 2:
            date_time = date_split[2].split(":")
            if date_time[0].count(" ") == 1:
                date_b = date_time[0].split(" ")
                if len(date_split[0]) == 4 and len(date_split[1]) == 2 and len(date_b[0]) == 2:
                    if len(date_b[1]) == 2 and len(date_time[1]) == 2 and len(date_time[2]) == 2:
                        return date
    if len(date) != 14:
        raise ValueError("Wrong date format")
    try:
        int(date)
    except ValueError:
        raise Exception("Wrong date format")
    return date[:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]


# Function:         Changes values in a time-series
# Note:             -
# Meaning input:    'time_series' is the time-series that is going to be changed;
#                   'dates' are the indexes; 'values' are the new values
# Meaning output:   None, 'time_series'-object gets changed directly
def set_values(time_series: pandas.Series, dates: List[str], values: List[float]) -> None:
    if len(dates) != len(values):
        warnings.warn("Length of dates does not equal length of values!")
    for date, value in zip(dates, values):
        time_series[convert_to_time_stamp(date)] = value


# Function:         Adds values to existing values in a time-series
# Note:             'values' can be a float. In that case, all dates are going to be changed by that value.
# Meaning input:    'time_series' is the time-series that is going to be changed;
#                   'dates' are the indexes; 'values' are the values that get added
# Meaning output:   None, 'time_series'-object gets changed directly
def change_values_by(time_series: pandas.Series, dates: List[str], values: Union[List[float], float]) -> None:
    if type(values) == list:
        if len(dates) != len(values):
            warnings.warn("Length of dates does not equal length of values!")
        for location, value in zip(dates, values):
            time_series[convert_to_time_stamp(location)] += value
    else:
        for location in dates:
            time_series[convert_to_time_stamp(location)] += values


# Function:         Multiples values in a time-series by a factor
# Note:             -
# Meaning input:    'time_series' is the time-series that is going to be changed;
#                   'dates' are the indexes; 'factor' is the factor, which gets multiplied
# Meaning output:   None, 'time_series'-object gets changed directly
def change_factor(time_series: pandas.Series, dates: List[str], factor: float) -> None:
    for location in dates:
        time_series[convert_to_time_stamp(location)] *= factor


# Function:         Sets given dates to NaN
# Note:             -
# Meaning input:    'time_series' is the time-series that is going to be changed; 'dates' are the indexes;
# Meaning output:   None, 'time_series'-object gets changed directly
def set_to_nan(time_series: pandas.Series, dates: List[str]) -> None:
    for location in dates:
        time_series[convert_to_time_stamp(location)] = nan


# Function:         Generates a list of timestamps
# Note:             'end_date' is not included, 'start_date' is included in the interval
# Meaning input:    Starting by 'start_date', ending by 'end_date', 'num' is the number of dates
# Meaning output:   'num' dates in a list, starting by 'start_date'
def create_interval_by_number(s_date: str, e_date: str, num: int) -> List[str]:
    interval = []
    start_date = convert_to_time_stamp(s_date)
    end_date = convert_to_time_stamp(e_date)
    if start_date == end_date:
        warnings.warn("Start date equals end date!")
        return [start_date for _ in range(num)]
    start_date_d = __convert_str_to_datetime(start_date)
    end_date_d = __convert_str_to_datetime(end_date)
    if num == 0:
        warnings.warn("'num' is equal to 0, empty list got returned!")
        return []
    elif num < 0:
        warnings.warn("'num' is not positive, empty list got returned!")
        return []
    frequency = (end_date_d - start_date_d) / num
    while start_date_d < end_date_d:
        interval.append(__convert_datetime_to_str(start_date_d))
        start_date_d += frequency
    return interval


# Function:         Generates a list of timestamps
# Note:             'end_date' is not included, 'start_date' is included in the interval
# Meaning input:    Starting by 'start_date', ending by 'end_date', ('fq_d', 'fq_h', 'fq_min', 'fq_sec') is
#                   the frequency of dates in days, hours, minutes and seconds
# Meaning output:   ((start date - end date) / frequency) dates in a list, starting by 'start_date'
def create_interval_by_freq(s_date: str, e_date: str, fq_d: int, fq_h: int, fq_min: int, fq_sec: int) -> List[str]:
    interval = []
    start_date = convert_to_time_stamp(s_date)
    end_date = convert_to_time_stamp(e_date)
    if start_date == end_date:
        warnings.warn("Start date equals end date!")
        return [start_date]
    start_date_d = __convert_str_to_datetime(start_date)
    end_date_d = __convert_str_to_datetime(end_date)
    if fq_d == fq_h and fq_h == fq_min and fq_min == fq_sec and fq_sec == 0:
        warnings.warn("Frequency is 0, empty list got returned!")
        return []
    elif fq_d < 0 or fq_h < 0 or fq_sec < 0 or fq_min < 0:
        warnings.warn("Frequency is not positive, empty list got returned!")
        return []
    frequency = datetime.timedelta(fq_d, fq_sec, 0, 0, fq_min, fq_h)
    while start_date_d < end_date_d:
        interval.append(__convert_datetime_to_str(start_date_d))
        start_date_d += frequency
    return interval


# Function:         Generates a new time series with old series and new data
# Note:             Returned time series is sorted
# Meaning input:    "time_series" is the old time series
#                   "values" is the list of new values added to the old time series
#                   "dates" are the corresponding dates
# Meaning output:   New time series
def add_points(time_series: pandas.Series, values: List[float], dates: List[str]) -> pandas.Series:
    for i in range(len(dates)):
        dates[i] = convert_to_time_stamp(dates[i])
    n = pandas.Series(values, dates).sort_index()
    return pandas.concat(time_series, n)


# Function:         Generates a new time series with old series and without specified dates
# Note:             -
# Meaning input:    "time_series" is the old time series
#                   "dates" are the to-be-removed dates
# Meaning output:   New time series
def remove_points(time_series: pandas.Series, dates: List[str]) -> pandas.Series:
    return time_series.drop(labels=dates)


# Function:         Finds all dates with value in "values"
# Note:             -
# Meaning input:    "time_series" is the time series
#                   "values" are the values
# Meaning output:   Returns all dates with value in "values"
def find_dates(time_series: pandas.Series, values: List[float]) -> List[str]:
    ret = []
    for date in time_series.index:
        if time_series[date] in values:
            ret.append(date)
    return ret


# Function:         Rotate points in time series. Moves "date" to "destination" by rotation values and dates
# Note:             -
# Meaning input:    "time_series" is the time series
#                   "date" is the to-be-moved date
#                   "destination" is the destination of rotation
# Meaning output:   Returns new time series
def move_point(time_series: pandas.Series, date: str, destination: str) -> pandas.Series:
    dates: List[str] = time_series.index.values.tolist()
    values: List[float] = time_series.values.tolist()
    index = dates.index(date)
    d_index = dates.index(destination)
    if d_index > index:
        temp = (date, values[index])
        while index < d_index:
            dates[index] = dates[index + 1]
            values[index] = values[index + 1]
            index += 1
        dates[d_index] = temp[0]
        values[d_index] = temp[1]
        return pandas.Series(values, dates)

    elif d_index < index:
        temp = (date, values[index])
        while index > d_index:
            dates[index] = dates[index - 1]
            values[index] = values[index - 1]
            index -= 1
        dates[d_index] = temp[0]
        values[d_index] = temp[1]
        return pandas.Series(values, dates)
    else:
        return time_series


# Function:         Creates a random peak in a time-series
# Note:             If 'values' is defined, 'min_value' and 'max_value' will be ignored.
# Meaning input:
# Meaning output:   None, 'time_series'-object gets changed directly
def create_peak(time_series: pandas.Series, values: Union[List[float], float] = None, min_value: float = None,
                max_value: float = None, num: int = 1, dates: List[str] = None) -> None:
    if dates is None:
        pos_dates = time_series.index
        picked_dates = []
        for i in range(num):
            picked_date = pos_dates[random.randint(0, len(pos_dates) - 1)]
            while picked_date in picked_dates:
                picked_date = pos_dates[random.randint(0, len(pos_dates) - 1)]
            picked_dates.append(picked_date)
        dates = picked_dates[:]
    if values is None:
        values = []
        if (min_value is None) and (max_value is None):
            min_value = max(time_series.values) * 2
            if min_value < 0:
                max_value = min_value
                min_value *= 2
            else:
                max_value = min_value * 2
        elif max_value is None:
            if min_value > 0:
                max_value = min_value * 2
            else:
                max_value = min_value / 2
        elif min_value is None:
            if max_value > 0:
                min_value = max_value / 2
            else:
                min_value = max_value * 2
        else:
            if min_value > max_value:
                raise Exception("Min value is bigger than max value!")
        for i in range(num):
            values.append(round(random.uniform(min_value, max_value), 1))
    change_values_by(time_series, dates, values)


# Function:         Converts values at given dates to a different format
# Note:             If date is None, one date will be picked randomly
# Meaning input:    'time_series' is the to-be-changed time_series; points are converted at the dates 'dates';
#                   'function' is the function for conversion
# Meaning output:   None, 'time_series'-object gets changed directly
def create_format_error(time_series: pandas.Series, dates: List[str] = None, function=str) -> None:
    dates_t: List[str] = time_series.index.values.tolist()
    if dates is None:
        date = dates_t[random.randint(0, len(dates_t) - 1)]
        time_series[date] = function(time_series[date])
    else:
        for date in dates:
            date = convert_to_time_stamp(date)
            time_series[date] = function(time_series[date])


def data_generate():
    # generate
    return [[1, 2, 3], ["21.10.2021", "22.10.2021", "23.10.2021"]]
