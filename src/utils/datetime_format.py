from datetime import datetime


def format_jira_date(dt: datetime) -> str:
    """
    Converts dates & times to the required Jira API string format.

    Args:
        dt: A datetime object.

    Returns:
        A string in the format 'YYYY-MM-DDTHH:MM:SS.000+0000'.
    """
    return dt.strftime(format="%Y-%m-%dT%H:%M:%S.000+0000")
