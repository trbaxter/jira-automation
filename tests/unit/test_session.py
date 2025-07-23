from unittest.mock import patch, MagicMock

from src.auth.session import get_authenticated_session
from tests.constants.patch_targets import (
    JAUTH_CERT_WHERE,
    JAUTH_GET_HEADER,
    JAUTH_REQ_SESSION
)


def test_get_authenticated_session_returns_configured_session() -> None:
    mock_session = MagicMock()
    mock_headers_obj = MagicMock()
    mock_session.headers = mock_headers_obj

    mock_cert_path = "/path/to/cert.pem"
    mock_headers = {
        "Authorization": "Basic encoded",
        "Content-Type": "application/json"
    }

    with (patch(JAUTH_REQ_SESSION, return_value=mock_session),
          patch(JAUTH_CERT_WHERE, return_value=mock_cert_path),
          patch(JAUTH_GET_HEADER, return_value=mock_headers)):
        result = get_authenticated_session()

        assert result is mock_session
        assert result.verify == mock_cert_path
        mock_headers_obj.update.assert_called_once_with(mock_headers)
