import logging
import requests

# Log errors in workflow during calls to Jira API
def handle_api_error(response: requests.Response, context: str) -> bool:
    if response.status_code not in [200, 201, 204]:
        logging.error(
            f"\nError during {context}. Status Code: {response.status_code}"
        )

        if response.status_code == 504:
            logging.error("Gateway timeout occurred.")

        else:
            logging.error(f"Response content: {response.text}")

        return False
    return True