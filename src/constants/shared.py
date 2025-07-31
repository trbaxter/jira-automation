"""
Type-level constraints and constants used throughout the application and
in test functions.

Includes reusable Pydantic validators and string patterns for consistent
field validation.
"""

from pydantic import conint, constr

JIRA_DATETIME_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$"
RESET = "\033[0m"
YELLOW_BOLD = "\033[1;33m"


# Integers
INT_GEQ_0 = conint(ge=0)
INT_GT_0 = conint(gt=0)

# Strings
JIRA_DATETIME_STR = constr(pattern=JIRA_DATETIME_REGEX)
SAFE_STR = constr(strip_whitespace=True, min_length=1)
