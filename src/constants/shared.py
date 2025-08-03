from pydantic import conint, constr


INT_GEQ_0 = conint(ge=0)
INT_GT_0 = conint(gt=0)
JIRA_DATETIME_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000\+\d{4}$"
JIRA_DATETIME_STR = constr(pattern=JIRA_DATETIME_REGEX)
SAFE_STR = constr(strip_whitespace=True, min_length=1)
