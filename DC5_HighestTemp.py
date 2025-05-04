import csv
from datetime import datetime
from collections import defaultdict

# Map function
def map_function(row):
    try:
        date = row[0]
        temp_max = float(row[2])
        temp_min = float(row[3])
        year = datetime.strptime(date, "%Y-%m-%d").year
        return (year, (temp_max, temp_min, 1))
    except:
        return None

# Reduce function
def reduce_function(mapped_data):
    reduced_data = defaultdict(lambda: {"max_sum": 0, "min_sum": 0, "count": 0})
    for item in mapped_data:
        if item:
            year, (tmax, tmin, count) = item
            reduced_data[year]["max_sum"] += tmax
            reduced_data[year]["min_sum"] += tmin
            reduced_data[year]["count"] += count
    return reduced_data

# Read CSV and apply map
mapped = []
with open("DC5_weather.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        mapped.append(map_function(row))

# Apply reduce
year_data = reduce_function(mapped)

# Find hottest and coolest year
hottest_year = None
coolest_year = None
max_avg_temp = float("-inf")
min_avg_temp = float("inf")

for year, data in year_data.items():
    avg_max = data["max_sum"] / data["count"]
    avg_min = data["min_sum"] / data["count"]

    if avg_max > max_avg_temp:
        max_avg_temp = avg_max
        hottest_year = year

    if avg_min < min_avg_temp:
        min_avg_temp = avg_min
        coolest_year = year

# Output
print(f"Hottest Year: {hottest_year} with avg max temperature {max_avg_temp:.2f}°C")
print(f"Coolest Year: {coolest_year} with avg min temperature {min_avg_temp:.2f}°C")
