from datetime import datetime, timedelta


def is_valid_dart_sprint(name: str, today: datetime) -> bool:
    """
    Validates whether a future sprint name follows the expected format
    expected by the department.

    Args:
        name: Name of a sprint.
        today: The current date.

    Returns:
        True if name matches "DART YYMMDD (MM/DD-MM/DD)", False otherwise.
    """
    yy = today.strftime("%y")
    mm = today.strftime("%m")
    dd = today.strftime("%d")
    end_date = today + timedelta(days=14)
    mmdd_today = today.strftime("%m/%d")
    mmdd_end = end_date.strftime("%m/%d")

    expected_prefix = f"DART {yy}{mm}{dd} ({mmdd_today}-{mmdd_end})"

    return name.strip() == expected_prefix
