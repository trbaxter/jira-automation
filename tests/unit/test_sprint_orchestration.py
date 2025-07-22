from unittest.mock import ANY
from unittest.mock import patch, MagicMock

import pytest

from src.orchestration.sprint_orchestration import automate_sprint
from tests.constants.patch_targets import (
    ORCH_CLOSE_SPRINT,
    ORCH_CREATE_NAME,
    ORCH_CREATE_SPRINT,
    ORCH_GET_SPRINT,
    ORCH_GET_STORIES,
    ORCH_MOVE_ISSUES,
    ORCH_START_SPRINT,
)
from tests.constants.test_constants import (
    ACTIVE,
    FUTURE,
    ISSUE1,
    MOCK_BASE_URL,
    MOCK_BOARD_NAME
)


@pytest.fixture
def mock_session():
    return MagicMock()


@patch(ORCH_START_SPRINT)
@patch(ORCH_MOVE_ISSUES)
@patch(ORCH_CLOSE_SPRINT)
@patch(ORCH_GET_STORIES)
@patch(ORCH_CREATE_SPRINT)
@patch(ORCH_GET_SPRINT)
@patch(ORCH_CREATE_NAME)
def test_use_future_backlog_sprint(
        _mock_generate_name,
        mock_get_state,
        mock_create,
        mock_get_issues,
        mock_close,
        mock_move_issues,
        mock_start_sprint,
        mock_session,
):
    def fake_get_sprint_by_state(session, config, state):
        if state == FUTURE:
            _ = session, config  # Unused, but required for function

            # Future backlog sprint
            return {
                "id": 100,
                "name": "DART 250721 (07/21-08/04)"
            }

        elif state == ACTIVE:
            return {
                "id": 99,
                "name": "DART 240707",
                "startDate": "2024-07-07T10:00:00.000Z",
                "endDate": "2024-07-21T10:00:00.000Z",
                "session": mock_session,
                "base_url": MOCK_BASE_URL
            }
        else:
            return None

    mock_get_state.side_effect = fake_get_sprint_by_state
    mock_get_issues.return_value = [{"key": ISSUE1}]

    automate_sprint(
        MOCK_BOARD_NAME,
        mock_session
    )

    mock_create.assert_not_called()
    mock_close.assert_called_once()
    mock_move_issues.assert_called_once()
    mock_start_sprint.assert_called_once_with(
        new_sprint_id=100,
        sprint_name="DART 250721 (07/21-08/04)",
        start_date=ANY, # datetime.now()
        end_date=ANY,   # datetime.now() + 2 weeks
        session=mock_session,
        base_url=MOCK_BASE_URL
    )

# @patch("src.orchestration.sprint_lifecycle.get_board_config")
# @patch("src.orchestration.sprint_lifecycle.get_sprint_by_state")
# @patch("src.orchestration.sprint_lifecycle.create_sprint")
# @patch("src.orchestration.sprint_lifecycle.get_incomplete_stories")
# @patch("src.orchestration.sprint_lifecycle.close_sprint")
# @patch("src.orchestration.sprint_lifecycle.move_issues_to_new_sprint")
# @patch("src.orchestration.sprint_lifecycle.start_sprint")
# @patch("src.orchestration.sprint_lifecycle.generate_sprint_name")
# def test_create_sprint_when_non_dart_future(
#         mock_generate_name,
#         mock_start_sprint,
#         mock_move_issues,
#         mock_close,
#         mock_create,
#         mock_get_state,
#         mock_get_config,
#         mock_session,
#         mock_config
# ):
#     # Mock non-DART future sprint
#     mock_get_config.return_value = mock_config
#     mock_get_state.side_effect = [
#         {"id": 1, "name": "Team Planning"},  # future
#         None  # active
#     ]
#     mock_create.return_value = {"id": 2}
#     mock_generate_name.return_value = "DART 250721 (07/21-08/04)"
#
#     automate_sprint(board_name="TEST", session=mock_session)
#
#     mock_create.assert_called_once()
#     mock_start_sprint.assert_called_once()
#     mock_move_issues.assert_not_called()
#     mock_close.assert_not_called()
