"""
Python 3.9
Pandas 1.3.2
Statistics is a built in library and its link
https://docs.python.org/3/library/statistics.html
"""

import time
import pandas as pd
from tabulate import tabulate

CITY_DATA = {'chicago': 'data/chicago.csv',
             'new york': 'data/new_york_city.csv',
             'washington': 'data/washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid
    # Inputs

    # Get user input for month (all, january, february, ... , june)

    # Get user input for day of week (all, monday, tuesday, ... sunday)

    city = input("Would you like to see data for Chicago, New York, or Washington?")
    while city.lower() not in CITY_DATA:
        city = input("Would you like to see data for Chicago, New York, or Washington? Correct input please")

    city = city.lower()

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    month, day = "all", "all"

    check = input("\nWould you like to filter the data by month, day, both, or not at all? Type \"none\" for no time "
                  "filter.")
    while True:
        if check.lower() != "month" and check.lower() != "day" and check.lower() != "both" and check.lower() != "none":
            print("\nPlease Enter Right inputs")
            check = input(
                "Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time "
                "filter.")
        else:
            break

    if check.lower() == "month" or check.lower() == "both":
        month = input("Which month? January, February, March, April, May, or June?")
        while True:
            if month.lower() not in months and month.lower() != "all":
                print("\nPlease Enter Right inputs")
                month = input("Which month? January, February, March, April, May, or June?")
            else:
                break
    if check.lower() == "day" or check.lower() == "both":
        day = input("Which day? (e.g., Sunday, Monday).")
        while True:
            if day.lower() not in days and day.lower() != "all":
                print("\nPlease Enter Right inputs")
                day = input("Which day? (e.g., Sunday, Monday).")
            else:
                break

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, hour, and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Hour'] = df['Start Time'].dt.hour
    # df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month_data = df.groupby(['Month']).size()
    popular_month = df['Month'].mode()[0]
    print("Most Popular Month: {}\nFrequency: {}\n".format(popular_month.title(),
                                                           popular_month_data[popular_month.title()]))

    # Display the most common day of week
    popular_day_data = df.groupby(['Day of Week']).size()
    popular_day = df['Day of Week'].mode()[0]
    print("Most Popular Day: {}\nFrequency: {}\n".format(popular_day, popular_day_data[popular_day]))

    # Display the most common start hour
    popular_hour_data = df.groupby(['Hour']).size()
    popular_hour = df['Hour'].mode()[0]
    print("Most Popular Hour: {}\nFrequency: {}\n".format(popular_hour, popular_hour_data[popular_hour]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_station = df.groupby(['Start Station']).size()
    print("Most Popular Start Station: {}\nFrequency: {}\n".format(popular_start_station,
                                                                   start_station[popular_start_station]))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_station = df.groupby(['End Station']).size()
    print("Most Popular End Station: {}\nFrequency: {}\n".format(popular_end_station, end_station[popular_end_station]))

    # Display most frequent combination of start station and end station trip
    station = df.groupby(['Start Station', 'End Station']).size()
    popular_station = station.idxmax()

    # station = df.groupby(['Start Station', 'End Station']).sum()
    print("Most Popular Trip:\n"
          "    Start Station: {}\n    End Station: {}\n    Frequency: {}".format(popular_station[0],
                                                                                 popular_station[1],
                                                                                 station[popular_station]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    df['Total Time'] = df['End Time'] - df['Start Time']
    total_time = df['Total Time'].sum()
    print("Total Time for Trip", total_time)

    # Display mean travel time
    mean_time = df['Total Time'].mean()
    print("mean Time for Trip", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # user = df.groupby(['User Type']).size()
    user_type = df['User Type'].value_counts()
    print("User Types:")
    for i, v in user_type.items():
        print("    ", i, ":", v)

    if city != "washington":
        # Display counts of gender
        # gen = df.groupby(['Gender']).size()
        genders = df['Gender'].value_counts()
        print("\nGenders:")
        for i, v in genders.items():
            print("    ", i, ":", v)

        # Display earliest, most recent, and most common year of birth
        # year = df.groupby(['Birth Year']).size()
        min_year = df['Birth Year'].min()
        max_year = df['Birth Year'].max()
        mode_year = df['Birth Year'].mode()

        print("\nEarliest Year:", int(min_year))
        print("Recent Year:", int(max_year))
        print("Most Common Year:", int(mode_year))
    else:
        print("\nThere is no birth year data for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = 'chicago', 'February', 'Sunday'
        df = load_data(city, month, day)
        print(pd.DataFrame(df['Start Station'].value_counts()).index)
        print("\nThe City is: {}, The Filter for Month is: {}, The Filter for Day is: {}".format(city.title(),
                                                                                                 month.title(),
                                                                                                 day.title()))
        re = input("\nIs this input right? Enter \'yes\' or \'no\'\n")
        if re.lower() == "no":
            main()
            break

        # time_stats(df)
        # station_stats(df)
        # trip_duration_stats(df)
        # user_stats(df, city)

        col = ["User ID", "Start Time", "End Time", "Trip Duration", "Start Station", "End Station",
               "User Type", "Gender", "Birth Year", "Month", "Hour", "Day of Week", "Total Time"]
        i, j = 0, 5
        while True:
            print(tabulate(df[i:j], headers=col, tablefmt='fancy_grid'))
            print('-' * 40)
            view = input("Would you like to see more data? Enter \'yes\' or \'no\'\n")
            j += 5
            i += 5
            if view.lower() != "yes":
                break

        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
