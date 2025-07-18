from datetime import datetime


# Format the start/end dates of generated sprints
def format_jira_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000+0000")