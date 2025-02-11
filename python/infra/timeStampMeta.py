from datetime import datetime, timezone


def utcDateTime(dateTime : datetime = None) -> datetime :
    if not dateTime:
        result = datetime.now(timezone.utc)
    else:
        result = dateTime.astimezone(timezone.utc)
    return result
    
def utcTimeStamp(dateTime : datetime = None) -> float:
    return utcDateTime(dateTime).timestamp()