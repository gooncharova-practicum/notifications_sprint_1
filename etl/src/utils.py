from datetime import datetime
from functools import lru_cache

import pytz


@lru_cache
def get_delay_in_ms(tz_: str, schedule_at: datetime) -> int:
    datetime_now_in_user_tz = datetime.now(tz=pytz.timezone(tz_)).replace(tzinfo=None)
    return int((schedule_at.replace(tzinfo=None) - datetime_now_in_user_tz).total_seconds() * 1000)
