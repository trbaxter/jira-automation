import logging

import requests

SUCCESS_CODES = {200, 201, 204}


def handle_api_error(response: requests.Response, context: str) -> bool:
    """
    Logs & evaluates HTTP call results to the Jira API.

    Checks whether the HTTP response was a successful request (200/201/204).
    If not successful, logs contextual info including the status code and
    details of the error. Also contains special handling for 504 timeouts.

    Args:
        response: The HTTP response object returned from a 'requests' call
                  to the Jira API.
        context: A descriptive label indicating the operation that was
                 performed (e.g. "closing sprint").

    Returns:
        True if successful, False otherwise.
    """
    if response.status_code not in SUCCESS_CODES:
        logging.error(
            "\nError during %s. Status Code: %d",
            context,
            response.status_code
        )

        if response.status_code == 504:
            logging.error("Gateway timeout occurred.")

        else:
            logging.error(
                "Response content: %s",
                response.text
            )

        return False
    return True
