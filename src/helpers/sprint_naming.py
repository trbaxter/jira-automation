from datetime import datetime

def generate_sprint_name(start_date: datetime, end_date: datetime) -> str:
    """
    Dynamically generates sprint names.

    Gets used if a new sprint isn't found in the backlog.
    Uses the following naming convention:
    <Some sprint name> <start date as YYMMDD> (start MM/DD - ending MM/DD)

    Args:
        start_date: The sprint's start date.
        end_date: The sprint's end date.

    Returns:
        str: A formatted sprint name as a string.
    """
    sprint_name = (
        f"<Sprint Name> {start_date.strftime('%y%m%d')} "
        f"({start_date.strftime('%m/%d')}-{end_date.strftime('%m/%d')})"
    )
    return sprint_name