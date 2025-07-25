class MissingSecretsError(Exception):
    """
    Raised when required repository secrets are missing.
    """

    def __init__(self, missing_vars: list[str]) -> None:
        msg = f"Missing required repository secrets: {', '.join(missing_vars)}"
        super().__init__(msg)
