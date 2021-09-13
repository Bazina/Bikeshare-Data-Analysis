import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")

CITY_DATA = {'Chicago': 'https://raw.githubusercontent.com/Bazina/Bikeshare-Data-Analysis/main/data/chicago.csv',
             'New York': 'https://raw.githubusercontent.com/Bazina/Bikeshare-Data-Analysis/main/data/new_york_city.csv',
             'Washington': 'https://raw.githubusercontent.com/Bazina/Bikeshare-Data-Analysis/main/data/washington.csv'}

# Use this if the server will be hosted locally through this command "streamlit run bikeshare-app.py"
# and the csv files in folder called data within the same directory of the app file
# CITY_DATA = {'Chicago': 'data/chicago.csv',
#              'New York': 'data/new_york_city.csv',
#              'Washington': 'data/washington.csv'}

months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

st.title("US Bikeshare Data Explorer!")

st.markdown("""
This app perform some statistics calculations on US bikeshare data.
- **Python Version:** 3.9.
- **Python Libraries:** Pandas 1.3.2, Matplotlib 3.4.3, Seaborn 0.11.2, Streamlit 0.88.0.
- **Data Source:** [CSV-Files](https://github.com/Bazina/Bikeshare-Data-Project/blob/main/data.7z).
""")

st.sidebar.header('User Input Features')
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

city = st.sidebar.radio("Would you like to see data for", ('Chicago', 'New York', 'Washington'))
check = st.sidebar.selectbox('Filter the data by', ['Both, Day & Month', 'Day', 'Month'])

if check == 'Both, Day & Month':
    month = st.sidebar.selectbox('Month', months)
    day = st.sidebar.selectbox('Day', days)
elif check == 'Day':
    month = 'All'
    day = st.sidebar.selectbox('Day', days)
else:
    month = st.sidebar.selectbox('Month', months)
    day = 'All'


def load_data(chosen_city, chosen_month, chosen_day):
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
    city_df = pd.read_csv(CITY_DATA[chosen_city])

    # convert the Start Time column to datetime
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
    city_df['End Time'] = pd.to_datetime(city_df['End Time'])

    # extract month, hour, and day of week from Start Time to create new columns
    city_df['Month'] = city_df['Start Time'].dt.month_name()
    city_df['Hour'] = city_df['Start Time'].dt.hour

    # df['Day of Week'] = df['Start Time'].dt.weekday_name
    city_df['Day of Week'] = city_df['Start Time'].dt.day_name()

    city_df['Total Time'] = city_df['End Time'] - city_df['Start Time']

    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        city_df = city_df[city_df['Month'] == chosen_month.title()]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        city_df = city_df[city_df['Day of Week'] == chosen_day.title()]

    if chosen_city != "Washington":
        col = ["User ID", "Start Time", "End Time", "Trip Duration", "Start Station", "End Station",
               "User Type", "Gender", "Birth Year", "Month", "Hour", "Day of Week", "Total Time"]

        city_df['Birth Year'].fillna(city_df['Birth Year'].mean(), inplace=True)
        city_df['Gender'].ffill(axis=0, inplace=True)

        city_df['Birth Year'] = city_df['Birth Year'].astype('int64')
    else:
        col = ["User ID", "Start Time", "End Time", "Trip Duration", "Start Station", "End Station",
               "User Type", "Month", "Hour", "Day of Week", "Total Time"]
    city_df.set_axis(col, axis=1, inplace=True)

    return city_df


df = load_data(city, month, day)
show_df = df.loc[:, :'Day of Week']

st.markdown("\nThe City is: {}, The Filter for Month is: {}, The Filter for Day is: {}".format(city.title(),
                                                                                               month.title(),
                                                                                               day.title()))

if st.button('Show Some Raw Data'):
    st.table(show_df.sample(n=5))

row3, row_spacer1, row4 = st.columns((1, 0.1, 1))


def time_stats(city_df):
    """Displays statistics on the most frequent times of travel."""

    st.markdown("""
    ### **Calculating The Most Frequent Times of Travel...**
    """)

    # Display the most common month
    popular_month_data = city_df.groupby(['Month']).size()
    popular_month = city_df['Month'].mode()[0]
    # st.markdown("  - **Most Popular Month:** {}\nFrequency: {}\n".format(popular_month.title(),
    #                                                                     popular_month_data[popular_month.title()]))

    # Display the most common day of week
    popular_day_data = city_df.groupby(['Day of Week']).size()
    popular_day = city_df['Day of Week'].mode()[0]
    # st.markdown("  - **Most Popular Day:** {}\nFrequency: {}\n".format(popular_day, popular_day_data[popular_day]))

    # Display the most common start hour
    popular_hour_data = city_df.groupby(['Hour']).size()
    popular_hour = city_df['Hour'].mode()[0]
    # st.markdown("  - **Most Popular Hour:** {}\nFrequency: {}\n".format(popular_hour,
    # popular_hour_data[popular_hour]))

    st.markdown("""| | Most Popular Month | Most Popular Day | Most Popular Hour |
                | ----------- | ----------- | ----------- | ----------- |
                | **Name/Number** | <span style="background:rgb(248, 249, 251);">*{}*</span> | <span style="background:rgb(248, 249, 251);">*{}*</span> | <span style="background:rgb(248, 249, 251);">*{}*</span> |
                | **Frequency** | <span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span> | <span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span> | <span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span> |""".format(
        popular_month.title(), popular_day, popular_hour,
        popular_month_data[popular_month.title()],
        popular_day_data[popular_day],
        popular_hour_data[popular_hour]), unsafe_allow_html=True)

    st.write("\n\n\n\n")
    if popular_hour > 12:
        pm_am = "p.m."
        st.markdown("Looks like the most traffic hour is "
                    '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251); font-weight:900">{} {}</span>'
                    ", and maybe this has a correlation with the age of the users. it looks like the bikers usually"
                    " start their session after the work-time which indicates that they trying"
                    " to have a good health".format(popular_hour - 12, pm_am),
                    unsafe_allow_html=True)
    else:
        pm_am = "a.m."
        st.markdown("Looks like the most traffic hour is "
                    '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251); font-weight:900">{} {}</span>'
                    ", and maybe this has a correlation with the age of the users. it looks like the bikers usually"
                    " start their session before the work-time which indicates that they trying"
                    " to have a good health".format(popular_hour, pm_am),
                    unsafe_allow_html=True)


def multiplt_hour(city_df):
    sns.set(style="ticks", context="talk", font_scale=0.4)
    st.subheader('Months vs Start Hours')
    if city_df.Month.nunique() > 1:
        g = sns.FacetGrid(city_df, col='Month', hue='Month', col_wrap=3)
        g.map(sns.histplot, "Hour", kde=True)
        st.pyplot(g)
    else:
        fig = plt.figure(figsize=(6, 4))
        sns.histplot(data=city_df, x='Hour', hue='Month', kde=True)
        st.pyplot(fig)


with row3:
    multiplt_hour(df)
    time_stats(df)


def station_stats(city_df):
    """Displays statistics on the most popular stations and trip."""

    st.markdown("""
    ### **Calculating The Most Popular Stations and Trip...**
    """)

    # Display most commonly used start station
    popular_start_station = city_df['Start Station'].mode()[0]
    start_station = city_df.groupby(['Start Station']).size()
    # st.markdown("  - **Most Popular Start Station:** {}\nFrequency: {}\n".format(popular_start_station,
    #                                                                             start_station[popular_start_station]))

    # Display most commonly used end station
    popular_end_station = city_df['End Station'].mode()[0]
    end_station = city_df.groupby(['End Station']).size()
    # st.markdown("  - **Most Popular End Station:** {}\nFrequency: {}\n".format(popular_end_station,
    #                                                                           end_station[popular_end_station]))

    st.markdown("""| | Most Popular Start Station | Most Popular End Station |
                    | ----------- | ----------- | ----------- | ----------- |
                    | **Name** | <span style="background:rgb(248, 249, 251);">*{}*</span> | <span style="background:rgb(248, 249, 251);">*{}*</span> |
                    | **Frequency** | <span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span> | <span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span> |""".format(
        popular_start_station,
        popular_end_station,
        start_station[popular_start_station],
        end_station[popular_end_station]), unsafe_allow_html=True)

    # Display most frequent combination of start station and end station trip
    station = city_df.groupby(['Start Station', 'End Station']).size()
    popular_station = station.idxmax()

    # station = df.groupby(['Start Station', 'End Station']).sum()
    st.markdown("  - **Most Popular Trip:**\n"
                "    - Start Station: "
                '<span style="font-style: italic; background:rgb(248, 249, 251);">{}</span>\n'
                "    - End Station: "
                '<span style="font-style: italic; background:rgb(248, 249, 251);">{}</span>\n'
                "    - Frequency: "
                '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**'
                '</span>'.format(popular_station[0],
                                 popular_station[1],
                                 station[popular_station]), unsafe_allow_html=True)


def station_plt(city_df):
    sns.set(style="ticks", context="talk", font_scale=0.4)
    st.subheader('Start Stations Frequencies')
    fig = plt.figure(figsize=(6, 4))
    ax = fig.subplots()
    data = pd.DataFrame(city_df['Start Station'].value_counts())
    sns.barplot(y=data['Start Station'][:5], x=data.index[:5], ax=ax, palette="rocket")
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Start Stations')
    plt.xticks(rotation=15)
    st.pyplot(fig)


with row4:
    station_plt(df)
    station_stats(df)


def trip_duration_stats(city_df):
    """Displays statistics on the total and average trip duration."""

    st.markdown("""
    ### **Calculating Trip Duration...**
    """)

    # Display total travel time

    total_time = city_df['Total Time'].sum()
    st.write("  - **Total Time for Trip is** ", total_time)

    # Display mean travel time
    mean_time = city_df['Total Time'].mean()
    st.write("  - **Mean Time for Trip is** ", mean_time)


trip_duration_stats(df)

row5_0, row5_1 = st.columns((1, 1))
row5, row_spacer2, row6 = st.columns((1, 0.1, 1))
row7, row8 = st.columns((1, 1))


def age(city_df):
    st.subheader('Users Ages')
    bin_edges = [1899, 1957, 1998, 2004, 2016]
    bin_names = ['Senior Adult (Old)', 'Adult', 'Adolescence', 'Child']
    city_df['Age Classification'] = pd.cut(city_df['Birth Year'], bin_edges, labels=bin_names)

    child = city_df[city_df['Age Classification'] == 'Child'].shape[0]
    adolescence = city_df[city_df['Age Classification'] == 'Adolescence'].shape[0]
    adult = city_df[city_df['Age Classification'] == 'Adult'].shape[0]
    old = city_df[city_df['Age Classification'] == 'Senior Adult (Old)'].shape[0]

    maxi = max(old, adult, adolescence, child)

    if maxi == child:
        cls = "children"
    elif maxi == adolescence:
        cls = "teenagers"
    elif maxi == adult:
        cls = "adults"
    else:
        cls = "senior adults (Old)"

    sns.set(style="ticks", context="talk", font_scale=0.6)
    fig = plt.figure(figsize=(6, 4))
    plt.bar(bin_names, [old, adult, adolescence, child])
    plt.ylim(0, maxi + 10000)
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    st.pyplot(fig)

    st.markdown("It looks like the major of bikers are **{}** about "
                '<span style="color:rgb(9, 171, 59); background:rgb(248, 249, 251); font-weight: 600;'
                ' font-style: italic;">{}</span>'
                " are between 13-18 "
                "years old among "
                '<span style="color:rgb(9, 171, 59); background:rgb(248, 249, 251); font-weight: 600;'
                ' font-style: italic;">{}</span>'.format(cls, adult, city_df.shape[0]), unsafe_allow_html=True)


def gender(city_df):
    st.subheader('Users Genders')
    sns.set(style="ticks", context="talk", font_scale=0.6)
    fig = plt.figure(figsize=(6, 4))
    male = city_df.query('Gender == "Male"').shape[0]
    female = city_df.query('Gender == "Female"').shape[0]
    plt.bar(['Male', 'Female'], [male, female])
    plt.ylim(0, max(male, female) + 10000)
    plt.xlabel('Genders')
    plt.ylabel('Frequency')
    plt.ylim(0, male + 10000)
    st.pyplot(fig)


def types(city_df):
    sns.set(style="ticks", context="talk", font_scale=0.6)
    st.subheader('Users Types')
    fig = plt.figure(figsize=(6, 4))
    sub = city_df[city_df['User Type'] == "Subscriber"].shape[0]
    cus = city_df[city_df['User Type'] == "Customer"].shape[0]
    dep = city_df[city_df['User Type'] == "Dependent"].shape[0]
    plt.bar(['Subscriber', 'Customer', 'Dependent'], [sub, cus, dep], color='darkred')
    plt.xlabel('User Types')
    plt.ylim(0, max(sub, cus, dep) + 10000)
    plt.ylabel('Frequency')
    st.pyplot(fig)


def user_stats(city_df, chosen_city):
    """Displays statistics on bikeshare users."""

    with row5_0:
        st.markdown("""
        ### **Calculating User Stats...**
        """)

    with row5:
        types(city_df)

        # Display counts of user types
        # user = df.groupby(['User Type']).size()
        user_type = city_df['User Type'].value_counts()

        type_user, cnt_user = [], []
        for i, v in user_type.items():
            type_user.append(i)
            cnt_user.append(v)

        if len(type_user) == 3:
            st.markdown("  - **User Types:**\n"
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span>\n'
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span>\n'
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**'
                        '</span>'.format(type_user[0], cnt_user[0], type_user[1], cnt_user[1], type_user[2],
                                         cnt_user[2]),
                        unsafe_allow_html=True)
        else:
            st.markdown("  - **User Types:**\n"
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span>\n'
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**'
                        '</span>'.format(type_user[0], cnt_user[0], type_user[1], cnt_user[1]),
                        unsafe_allow_html=True)

        if cnt_user[0] > cnt_user[1]:
            typ = "Subscriber"
        else:
            typ = "Customer"
        st.markdown("Notice that the dominated **type** is "
                    '<span style="background:rgb(248, 249, 251);">*{}*'
                    '</span>'.format(typ), unsafe_allow_html=True)

    with row6:
        if chosen_city != "Washington":
            gender(city_df)

            # Display counts of gender
            # gen = df.groupby(['Gender']).size()
            genders = city_df['Gender'].value_counts()

            type_gender, cnt_gender = [], []
            for i, v in genders.items():
                type_gender.append(i)
                cnt_gender.append(v)

            st.markdown("  - **Genders:**\n"
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**</span>\n'
                        "    - {}: "
                        '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251);">**{}**'
                        '</span>'.format(type_gender[0],
                                         cnt_gender[0],
                                         type_gender[1],
                                         cnt_gender[1]),
                        unsafe_allow_html=True)

            if cnt_gender[0] > cnt_gender[1]:
                sex = "Male"
                st.markdown("Notice that the dominated **gender** is "
                            '<span style="color:rgb(80, 106, 212); background:rgb(248, 249, 251); font-weight:900">{}'
                            '</span>'.format(sex), unsafe_allow_html=True)
            else:
                sex = "Female"
                st.markdown("Notice that the dominated **gender** is "
                            '<span style="color:rgb(187, 32, 32); background:rgb(248, 249, 251); font-weight:900">{}'
                            '</span>'.format(sex), unsafe_allow_html=True)

    if chosen_city != "Washington":
        with row7:
            age(city_df)

        # Display earliest, most recent, and most common year of birth
        # year = df.groupby(['Birth Year']).size()
        min_year = city_df['Birth Year'].min()
        max_year = city_df['Birth Year'].max()
        mode_year = city_df['Birth Year'].mode()[0]

        col1, col_space1, col2, col_space2, col3 = st.columns((1, 0.1, 1, 0.1, 1))

        with col1:
            st.markdown("\n  - **Earliest Year:** "
                        '<span style="color:rgb(9, 171, 59); background:rgb(248, 249, 251); font-weight: 600;'
                        ' font-style: italic;">{}</span>'.format(min_year),
                        unsafe_allow_html=True)

        with col2:
            st.markdown("  - **Recent Year:** "
                        '<span style="color:rgb(9, 171, 59); background:rgb(248, 249, 251); font-weight: 600;'
                        ' font-style: italic;">{}</span>'.format(max_year),
                        unsafe_allow_html=True)
        with col3:
            st.markdown("  - **Most Common Year:** "
                        '<span style="color:rgb(9, 171, 59); background:rgb(248, 249, 251); font-weight: 600;'
                        ' font-style: italic;">{}</span>'.format(mode_year),
                        unsafe_allow_html=True)
    else:
        st.markdown('\n<span style="color:rgb(187, 32, 32); font-size:1.5em; background:rgb(248, 249, 251);">'
                    '**There is no birth year and genders data for this city**</span>',
                    unsafe_allow_html=True)


user_stats(df, city)
