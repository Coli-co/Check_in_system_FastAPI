from datetime import datetime
import pytz


async def get_utc_in_milliseconds_from_taipei_time(taipei_date_time):
    if not taipei_date_time:
        return None

    # Define the time zone for Taipei
    taipei_timezone = pytz.timezone('Asia/Taipei')

    # Convert the input Taipei time to a datetime object
    taipei_time = datetime.strptime(taipei_date_time, '%Y-%m-%d %H:%M')
    taipei_time = taipei_timezone.localize(taipei_time)

    # Convert to UTC+0 time
    utc_time = taipei_time.astimezone(pytz.utc)

    # Get the time in milliseconds
    milliseconds = int(utc_time.timestamp() * 1000)

    return milliseconds


# Example usage:
# taipei_datetime = '2023-09-20 14:30'
# result = get_utc_in_milliseconds_from_taipei_time(taipei_datetime)
# print(result)
