from datetime import datetime, timezone


def utc_time():
    return datetime.now(timezone.utc)


def utc_time_ns():
    return int(utc_time().timestamp() * 1e9)


def utc_time_iso():
    return utc_time().isoformat()
