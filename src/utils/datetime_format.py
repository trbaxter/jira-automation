from datetime import datetime


def format_jira_date(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000+0000')
