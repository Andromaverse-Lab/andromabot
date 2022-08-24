
from datetime import timedelta


def relative_time(td: timedelta) -> str:
    seconds = td.total_seconds()
    if seconds < 45:
        return "less than a minute ago"
    if seconds < 90:
        return "about a minute ago"
    if seconds < 60 * 45:
        return f"about {round(seconds/60)} minutes ago"
    if seconds < 60 * 60 * 1.25:
        return f"about an hour ago"
    if seconds < 60 * 60 * 1.75:
        return f"about 1.5 hours ago"
    if seconds < 60 * 60 * 24:
        return f"about {round(seconds/60/60)} hours ago"
    return f"over a day ago"
