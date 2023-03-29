from datetime import datetime, timezone

def str2epoch(x: str) -> int:
    return str2datetime(x).timestamp()

def str2datetime(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

def epoch2datetime(epoch: int) -> datetime:
    return datetime.fromtimestamp(epoch).replace(tzinfo=timezone.utc)