from datetime import datetime

from src.customtypes.shared import SAFE_STR


def generate_sprint_name(start_date: datetime, end_date: datetime) -> SAFE_STR:
    sprint_name = (
        f'DART {start_date.strftime('%y%m%d')} '
        f'({start_date.strftime('%m/%d')}-{end_date.strftime('%m/%d')})'
    )
    return sprint_name
