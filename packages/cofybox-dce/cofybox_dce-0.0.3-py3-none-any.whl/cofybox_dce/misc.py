import pandas as pd


def iso8601z(timestamp: pd.Timestamp) -> str:
    """
    Convert Timestamp to ISO8601-notation in UTC with "Z" suffix
    """
    timestamp = timestamp.tz_convert('UTC')
    iso = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
    return iso
