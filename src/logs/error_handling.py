import logging

import requests

SUCCESS_CODES = {200, 201, 204}

def handle_api_error(response: requests.Response, context: str) -> bool:
    if response.status_code not in SUCCESS_CODES:
        logging.error(
            f"\nError during {context}. Status Code: {response.status_code}"
        )

        if response.status_code == 504:
            logging.error("Gateway timeout occurred.")

        else:
            logging.error(f"Response content: {response.text}")

        return False
    return True
