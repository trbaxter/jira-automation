# Config Accessor
GET_HELPERS_BOARD_CONFIG = "src.helpers.config_accessor.get_board_config"


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
BOARD_CONFIG = "src.orchestration.sprint_orchestration.get_board_config"


# Sprint Transfer
MOVE_ISSUES = "src.services.sprint_transfer.move_issues_to_new_sprint"