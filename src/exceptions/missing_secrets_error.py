class MissingSecretsError(Exception):
    """
    Raised when required JIRA credentials are missing from repository secrets.
    """

    def __init__(self, missing_vars: list[str]) -> None:
        msg = f"Missing required repository secrets: {', '.join(missing_vars)}"
        super().__init__(msg)
