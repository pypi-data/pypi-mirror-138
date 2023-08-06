from datetime import time, datetime

class Prayer:
    """Individual prayer object"""
    def __init__(self, name:str, time:time):
        self.name = name
        self.time = time

class Day:
    """Day object, list of Prayer objects"""
    def __init__(self, fajr:time, dhor:time, asr:time, maghreb:time, icha:time, date : datetime):
        self.fajr = Prayer("fajr", fajr)
        self.dhor = Prayer("dhor", dhor)
        self.asr = Prayer("asr", asr)
        self.maghreb = Prayer("maghreb", maghreb)
        self.icha = Prayer("icha", icha)
        self.date = date

    def __str__(self) -> str:
        """Returns a string to show the daily prayers"""
        string = f"Date : {self.date} \n{self.fajr.name} : {self.fajr.time}\n{self.dhor.name} : {self.dhor.time} \n{self.asr.name} : {self.asr.time}\n{self.maghreb.name} : {self.maghreb.time} \n{self.icha.name} : {self.icha.time}"
        return string

    def next_prayer(self, time = datetime.now().time()) -> Prayer:
        """Returns an object of the next prayer, based on current time of the system"""
        if time <= self.fajr.time:
            return self.fajr
        elif time <= self.dhor.time:
            return self.dhor
        elif time <= self.asr.time:
            return self.asr
        elif time <= self.maghreb.time:
            return self.maghreb
        elif time <= self.icha.time:
            return self.icha
        else:
            return None