"""Here is where the magic happens ;). The main file."""
from datetime import time, datetime
from json.decoder import JSONDecodeError
import requests
from multipledispatch import dispatch
from requests.models import Response
from .Entities import Day

##Declaring needed variables
BASE_URL = "https://api.pray.zone/v2/times/"
URL_TODAY = BASE_URL+"today.json"
URL_THIS_MONTH = BASE_URL+"this_month.json"
URL_DATE = BASE_URL+"dates.json"
URL_DAY = BASE_URL+"day.json"
VALUE_ERROR_STRING = "One of the parameters you've entered is in the wrong type. Please refer to the documentation."


def parse_date_to_string(date_object:datetime) -> Response:
    return f"{date_object.year}-{date_object.month}-{date_object.day}"

@dispatch(str, int, int, int, str)
def request_builder(city:str, school:int, juristic:int, timeformat:int, url:str) -> Response:
    """Creates the request with correct url and parameters"""
    params = {'city': city, 'school': school, 'juristic':juristic, 'timeformat': timeformat}
    request = requests.get(url = url, params=params)
    return request

@dispatch(str, int, int, int, str, datetime)
def request_builder(city:str, school:int, juristic:int, timeformat:int, url:str, date_object:datetime) -> Response:
    """Creates the request with correct url and parameters"""
    start = parse_date_to_string(date_object)
    params = {'city': city, 'school': school, 'juristic':juristic, 'timeformat': timeformat, 'date' : start}
    request = requests.get(url = url, params=params)
    return request

@dispatch(str, int, int, int, str, datetime, datetime)
def request_builder(city, school:int, juristic:int, timeformat:int, url:str, start_date: datetime, end_date: datetime) -> Response:
    """Creates the request with correct url and parameters"""
    start = parse_date_to_string(start_date)
    end = parse_date_to_string(end_date)
    params = {'city': city, 'school': school, 'juristic':juristic, 'timeformat': timeformat, 'start' : start, 'end': end}
    request = requests.get(url = url, params=params)
    return request

def format_time(temp_salat: str) -> time:
    """Format string hours to time object"""
    (hour, minut) = temp_salat.split(':')
    salat = time(hour=int(hour), minute=int(minut))
    return salat

def get_today_prayer(request: Response) -> Day:
    """Returns today prayer"""
    try:
        data = request.json()
    except JSONDecodeError:
        raise ValueError(VALUE_ERROR_STRING)
    times = data["results"]["datetime"][0]["times"]
    dates = data["results"]["datetime"][0]["date"]["gregorian"]
    return parse_day_prayer(times, dates)

def string_to_date(date_str:str) -> datetime:
    """Parse date string in date object"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj

def parse_day_prayer(day_object, dates) -> Day:
    """Returns a Day object with given parameters"""
    day_date = string_to_date(dates)
    prayer = Day(format_time(day_object["Fajr"]), format_time(day_object["Dhuhr"]),
        format_time(day_object["Asr"]), format_time(day_object["Maghrib"]),
        format_time(day_object["Isha"]), day_date)
    return prayer

def get_month_prayer(request : Response) -> list:
    """Returns a list of the monthly prayers as a list of days"""
    month_list = []
    data = request.json()
    month = data["results"]["datetime"]
    for day in month:
        month_list.append(parse_day_prayer(day["times"], day["date"]["gregorian"]))
    return month_list

class PrayerTimes:
    """Prayer times API implementation class

    You have to create an instance of Prayer_times to use this API. For more information : https://pypi.org/project/prayer-tool/

    :param CITY: The city from where you need the calendar.
                        For example ``Brussels``
    :type CITY: string

    :param SCHOOL: Every school have a different calculation, we use 3 by default (Muslim World League).
                        For example 3
    :type SCHOOL: int

    :param JURISTIC: 0 for Shafii (or the standard way), 1 for Hanafi. If you leave this empty, it defaults to Shafii.
                        For example 0
    :type JURISTIC: int
    """

    def __init__(self, city:str ="Brussels", school:int =3, juristic:int =0):
        if isinstance(city, str) and isinstance(school, int) and isinstance(juristic, int):
            self.city = city
            self.school = school
            self.juristic = juristic
            self.timeformat = 0
        else:
            raise ValueError(VALUE_ERROR_STRING)

    @dispatch()
    def get_date(self) -> Day:
        """returns today's prayer"""
        request = request_builder(self.city, self.school, self.juristic, self.timeformat, URL_TODAY)
        return get_today_prayer(request)

    @dispatch(datetime)
    def get_date(self, this_date: datetime) -> Day:
        """Get the Day schedule of a precise date"""
        request = request_builder(self.city, self.school, self.juristic, self.timeformat, URL_DAY, this_date)
        return get_month_prayer(request)[0]

    @dispatch(datetime, datetime)
    def get_date(self, start: datetime, end: datetime) -> list:
        """Get the Day list for a dates interval"""
        request = request_builder(self.city, self.school, self.juristic, self.timeformat, URL_DATE, start, end)
        return get_month_prayer(request)
