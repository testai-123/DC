import csv
from datetime import datetime
from collections import defaultdict

# Simulate Map step
year_data = defaultdict(lambda: {"max_sum": 0, "min_sum": 0, "count": 0})

with open("weather.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        try:
            date = row[0]
            temp_max = float(row[2])
            temp_min = float(row[3])
            year = datetime.strptime(date, "%Y-%m-%d").year

            year_data[year]["max_sum"] += temp_max
            year_data[year]["min_sum"] += temp_min
            year_data[year]["count"] += 1
        except:
            continue

# Simulate Reduce step
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
