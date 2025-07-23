# Config Accessor
CONFIG_ACCESS_GET_CONFIG = "src.helpers.config_accessor.get_board_config"
CONFIG_ACCESS_LOAD_CONFIG = "src.helpers.config_accessor.load_config"


# Jira Auth
JAUTH_CERT_WHERE = "src.auth.session.certifi.where"
JAUTH_GET_CREDS = "src.auth.jira_auth.get_jira_credentials"
JAUTH_GET_HEADER = "src.auth.session.get_auth_header"
JAUTH_MAKE_TOKEN = "src.auth.jira_auth.make_basic_auth_token"
JAUTH_REQ_SESSION = "src.auth.session.requests.Session"


# Jira Issues Service
GET_INCOMPLETE_STORIES = "src.services.jira_issues.get_incomplete_stories"
JIRA_ISSUES_HANDLE_API_ERROR = "src.services.jira_issues.handle_api_error"


# Jira Sprint Closure
JCLOSE_BUILD_PAYLOAD = (
    "src.services.jira_sprint_closure.build_close_sprint_payload"
)
JCLOSE_CLOSE_SPRINT = "src.services.jira_sprint_closure.close_sprint"
JCLOSE_HANDLE_ERROR = "src.services.jira_sprint_closure.handle_api_error"


# Jira Sprint Service
JSPRINT_GET_CONFIG = "src.services.jira_sprint.get_board_config"
JSPRINT_HANDLE_ERROR = "src.services.jira_sprint.handle_api_error"
JSPRINT_PARSE_RESPONSE = "src.services.jira_sprint.parse_json_response"
JSPRINT_POST_PAYLOAD = "src.services.jira_sprint.post_sprint_payload"
CREATE_SPRINT = "src.services.jira_sprint.create_sprint"
GET_SPRINT_BY_STATE = "src.services.jira_sprint.get_sprint_by_state"


# Jira Sprint Start
JSTART_HANDLE_ERROR = "src.services.jira_start_sprint.handle_api_error"
JSTART_START_SPRINT = "src.services.jira_start_sprint.start_sprint"


# Payload Builder
PAYLOAD_BUILDER_FORMAT_DATE = "src.helpers.payload_builder.format_jira_date"


# Sprint Naming
CREATE_SPRINT_NAME = "src.helpers.sprint_naming.generate_sprint_name"


# Sprint Orchestration
ORCH_BOARD_CONFIG = "src.orchestration.sprint_orchestration.get_board_config"
ORCH_CLOSE_SPRINT = "src.orchestration.sprint_orchestration.close_sprint"
ORCH_CREATE_NAME = "src.orchestration.sprint_orchestration.generate_sprint_name"
ORCH_CREATE_SPRINT = "src.orchestration.sprint_orchestration.create_sprint"
ORCH_GET_SPRINT = "src.orchestration.sprint_orchestration.get_sprint_by_state"
ORCH_GET_STORIES = (
    "src.orchestration.sprint_orchestration.get_incomplete_stories"
)
ORCH_MOVE_ISSUES = (
    "src.orchestration.sprint_orchestration.move_issues_to_new_sprint"
)
ORCH_START_SPRINT = "src.orchestration.sprint_orchestration.start_sprint"


# Sprint Transfer
XFER_BATCH_ALL = "src.services.sprint_transfer.transfer_all_issue_batches"
XFER_EXTRACT_KEYS = "src.services.sprint_transfer.extract_issue_keys"
XFER_HANDLE_ERROR = "src.services.sprint_transfer.handle_api_error"
XFER_LOGGING = "src.services.sprint_transfer.logging"
XFER_MOVE_ISSUES = "src.services.sprint_transfer.move_issues_to_new_sprint"
XFER_RETRY = "src.services.sprint_transfer.transfer_issue_batch_with_retry"