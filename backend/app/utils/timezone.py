from datetime import datetime
from zoneinfo import ZoneInfo


def get_kst_now():
    """Returns the current time in KST (Asia/Seoul)."""
    return datetime.now(ZoneInfo("Asia/Seoul"))
