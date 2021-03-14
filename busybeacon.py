import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz

# Replace this with the URL template corresponding to your calendar's events
GCALENDAR_URL_TEMPLATE = "https://clients6.google.com/calendar/v3/calendars/email@gmail.com/events?calendarId=email%40gmail.com&singleEvents=true&timeZone={timezone}&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin={start_datetime}&timeMax={end_datetime}&key=AIzaSxBNlYH01_8Hc5S1J9vuBZJNAXxs"
LOCAL_TIMEZONE = "America/New_York"  # Replace this with your time zone.

def get_busy_times_from_google_calendar():
    """Returns a list of tuples (start time, end time) that represent busy times."""

    # Headers for the HTTP GET request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    # Define a function encode which will take a string as input and return a
    # URL-safe version. For example: "America/New_York" is converted to
    # "America%2FNew_York".
    encode = lambda string: urllib.parse.quote(string, safe="")

    # Get the time at the start of the current day (midnight) in this timezone.
    timezone = pytz.timezone(LOCAL_TIMEZONE)
    start_of_today = timezone.localize(datetime.now()).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_of_tomorrow = start_of_today + timedelta(days=1)

    # Generate the URL with the timezone, start date, and end date parameters.
    url = GCALENDAR_URL_TEMPLATE.format(
        timezone=encode(LOCAL_TIMEZONE),
        start_datetime=encode(start_of_today.isoformat()),
        end_datetime=encode(start_of_tomorrow.isoformat()),
    )

    # Send the request, get the response, parse it.
    response = requests.get(url, headers=headers)
    parsed_response = json.loads(response.text)

    # Get the start and end times from all of the events.
    busy_times = []
    for event in parsed_response["items"]:
        event_start = datetime.fromisoformat(event["start"]["dateTime"])
        event_end = datetime.fromisoformat(event["end"]["dateTime"])

        # Do not include all-day events.
        if event_end - event_start == timedelta(days=1):
            continue
        
        busy_times.append((event_start, event_end))

    return busy_times
    