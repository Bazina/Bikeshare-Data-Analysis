# Bikeshare-Data-Project
- In this project, Python is used to explore data related to bike share systems for three major cities in the 
United States—Chicago, New York City, and Washington.
A code is written to import the data and answer interesting questions
the user will ask about it by computing descriptive statistics.

## Table of Contents

- [Used-Languages](#Used-Languages)
- [Libraries](#Libraries)
- [Used-Data](#Used-Data)
- [Instructions](#Instructions)
- [What-It-Does](#What-It-Does)

### Used-Languages
- `Python 3.9`

### Libraries
- `Pandas 1.3.2`
- `time`
- `tabulate`

### Used Data
- #### History
  - **Motivate** provided this data.
  - *Over the past decade*, bicycle-sharing systems have been growing in number and popularity in cities across the world.
    - Bicycle-sharing systems allow users to rent bicycles on a very short-term basis for a price.
    This allows people to borrow a bike from *point A* and return it at *point B*,
    though they can also return it to the *same location* if they'd like to just go for a ride.
  - Regardless, each bike can serve *several users per day*.
- #### What The Data Looks Like
  - Randomly selected data for the first six months of 2017 are provided for all three cities.
  All three of the data files contain the same core **6** columns:
    1. **Start Time** (e.g., 2017-01-01 00:07:57)
    2. **End Time** (e.g., 2017-01-01 00:20:53)
    3. **Trip Duration** (in seconds - e.g., 776)
    4. **Start Station** (e.g., Broadway & Barry Ave)
    5. **End Station** (e.g., Sedgwick St & North Ave)
    6. **User Type** (Subscriber or Customer)

  - The Chicago and New York City files also have the following two columns:
    1. **Gender**
    2. **Birth Year**

### Instructions
- Run the script through the cmd or terminal using the following lines:
  1. Go to the folder where the script is: `cd /[drive] [the whole path]`. **(e.g., cd /d D:\Bikeshare Data Project)**
  2. Run the script in the **cmd** `python3 bikeshare.py`. **(e.g., python3 bikeshare.py)**
- The **Comments** in the script is *important*, and it helps to understand the code.

### What It Does
1. Calculates the most frequent times of travel:
   - Most popular month, day, and hour.
2. Calculate the most popular stations and trip:
   - Most popular start station, end station, trip
3. Calculates the trip duration of the whole data:
   - The total time, and the time average.
4. Calculates the user stats like:
   - Type: subscriber or customer.
   - Gender: male or female.
5. Gets the oldest, youngest, and the most common year in this data (only for Chicago and New York)
6. Gives some Data of the filtered data the users chooses.
