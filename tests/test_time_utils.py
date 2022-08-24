from andromabot.time_utils import relative_time
from datetime import timedelta

def test_relative_time_under_a_minute():
    td = timedelta(seconds=5)
    assert relative_time(td) == "less than a minute ago"

def test_relative_time_about_a_minute():
    td = timedelta(minutes=1)
    assert relative_time(td) == "about a minute ago"

    td = timedelta(minutes=1, seconds=25)
    assert relative_time(td) == "about a minute ago"

def test_relative_time_minutes():
    td = timedelta(minutes=2)
    assert relative_time(td) == "about 2 minutes ago"

    td = timedelta(minutes=43)
    assert relative_time(td) == "about 43 minutes ago"

def test_relative_time_hour():
    td = timedelta(minutes=52)
    assert relative_time(td) == "about an hour ago"

    td = timedelta(hours=1, minutes=10)
    assert relative_time(td) == "about an hour ago"

def test_relative_time_hour_and_half():
    td = timedelta(hours=1, minutes=30)
    assert relative_time(td) == "about 1.5 hours ago"

def test_relative_time_hours():
    td = timedelta(hours=2)
    assert relative_time(td) == "about 2 hours ago"

    td = timedelta(hours=4, minutes=2)
    assert relative_time(td) == "about 4 hours ago"

def test_relative_time_days():
    td = timedelta(days=1)
    assert relative_time(td) == "over a day ago"
