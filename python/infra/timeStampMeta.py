from datetime import datetime, timezone
from typing import Optional

def utcDateTime(dateTime : Optional[datetime] = None) -> datetime :
    if not dateTime:
        result = datetime.now(timezone.utc)
    else:
        result = dateTime.astimezone(timezone.utc)
    return result
    
def utcTimeStamp(dateTime : Optional[datetime] = None) -> float:
    return utcDateTime(dateTime).timestamp()