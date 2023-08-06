from prayer_tool import Prayer_times
import datetime

#Declaring an instance
instance = Prayer_times.PrayerTimes(city="Paris")

#The datetime objects we need
start = datetime.datetime(year = 2021, month = 9, day = 16)
end = datetime.datetime(year = 2021, month = 9, day = 17)

#Call the function and save the result
result = instance.get_date(start, end)

for item in result:
    print(item.__str__() + "\n")

