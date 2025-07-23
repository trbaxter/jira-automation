from unittest.mock import ANY, MagicMock, patch

import pytest

from src.orchestration.sprint_orchestration import automate_sprint
from tests.constants.patch_targets import (
    ORCH_CLOSE_SPRINT,
    ORCH_CREATE_NAME,
    ORCH_CREATE_SPRINT,
    ORCH_GET_SPRINT,
    ORCH_GET_STORIES,
    ORCH_MOVE_ISSUES,
    ORCH_START_SPRINT
)
from tests.constants.test_constants import (
    ACTIVE,
    FUTURE,
    MOCK_BASE_URL,
    MOCK_BOARD_NAME
)

# Note: @patch listing in alphabetical order
@patch(ORCH_CLOSE_SPRINT)
@patch(ORCH_CREATE_NAME)
@patch(ORCH_CREATE_SPRINT)
@patch(ORCH_GET_SPRINT)
@patch(ORCH_GET_STORIES)
@patch(ORCH_MOVE_ISSUES)
@patch(ORCH_START_SPRINT)
class TestAutomateSprint:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_session = MagicMock()

    def test_use_future_backlog_sprint(
            self,
            mock_start_sprint,
            mock_move_issues,
            mock_get_stories,
            mock_get_sprint,
            mock_create_sprint,
            _mock_create_name,
            mock_close_sprint,
    ):
        def fake_get_sprint_by_state(
                session: MagicMock,
                config: dict,
                state: str
        ) -> dict | None:
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
                    "session": self.mock_session,
                    "base_url": MOCK_BASE_URL
                }
            else:
                return None

        mock_get_sprint.side_effect = fake_get_sprint_by_state
        mock_get_stories.return_value = [{"key": "Issue_1"}]

        automate_sprint(MOCK_BOARD_NAME, self.mock_session)

        mock_create_sprint.assert_not_called()
        mock_close_sprint.assert_called_once()
        mock_move_issues.assert_called_once()
        mock_start_sprint.assert_called_once_with(
            100,
            "DART 250721 (07/21-08/04)",
            ANY,  # datetime.now()
            ANY,  # datetime.now() + 2 weeks
            self.mock_session,
            MOCK_BASE_URL
        )

    def test_automate_sprint_create_new_sprint(
            self,
            mock_start_sprint,
            mock_move_issues,
            _mock_get_stories,
            mock_get_sprint,
            mock_create_sprint,
            mock_create_name,
            mock_close_sprint,
    ):
        def fake_get_sprint(
                session: MagicMock,
                config: dict,
                state: str
        ) -> dict | None:
            _ = session, config  # Unused, but required for function

            if state == FUTURE:
                return {"id": 1, "name": "Non-DART Sprint"}
            if state == ACTIVE:
                return None
            return None

        mock_get_sprint.side_effect = fake_get_sprint
        mock_create_sprint.return_value = {"id": 2}
        mock_create_name.return_value = "DART 250721 (07/21-08/04)"

        automate_sprint("TEST", self.mock_session)

        mock_create_sprint.assert_called_once()
        mock_start_sprint.assert_called_once()
        mock_close_sprint.assert_not_called()
        mock_move_issues.assert_not_called()

    def test_log_if_no_future_sprint_creates_dart(
            self,
            mock_start_sprint,
            _mock_move_issues,
            _mock_get_stories,
            mock_get_sprint,
            mock_create_sprint,
            mock_create_name,
            _mock_close_sprint,
            caplog
    ):
        def fake_get_sprint(
                session: MagicMock,
                config: dict,
                state: str
        ) -> None:
            _ = session, config  # Unused, but required for function

            if state == FUTURE:
                return None
            if state == ACTIVE:
                return None
            return None

        mock_get_sprint.side_effect = fake_get_sprint
        mock_create_name.return_value = "DART 250721 (07/21-08/04)"
        mock_create_sprint.return_value = {"id": 123}

        with caplog.at_level("INFO"):
            automate_sprint("TEST", self.mock_session)

        assert "No upcoming sprint found" in caplog.text
        mock_create_sprint.assert_called_once()
        mock_start_sprint.assert_called_once()

    def test_log_if_create_sprint_returns_none(
            self,
            mock_start_sprint,
            _mock_move_issues,
            _mock_get_stories,
            mock_get_sprint,
            mock_create_sprint,
            mock_create_name,
            _mock_close_sprint,
            caplog
    ):
        def fake_get_sprint(
                session: MagicMock,
                config: dict,
                state: str
        ) -> None:
            _ = session, config  # Unused, but required for function

            if state == FUTURE:
                return None
            if state == ACTIVE:
                return None
            return None

        mock_get_sprint.side_effect = fake_get_sprint
        mock_create_name.return_value = "DART 250721 (07/21-08/04)"
        mock_create_sprint.return_value = None

        with caplog.at_level("ERROR"):
            automate_sprint("TEST", self.mock_session)

        assert "Failed to create a new sprint." in caplog.text
        mock_start_sprint.assert_not_called()
