from src.helpers.payload_builder import build_close_sprint_payload

def test_build_close_sprint_payload_returns_expected_dict() -> None:
    name = "Sprint X"
    start = "2025-08-01T00:00:00.000Z"
    end = "2025-08-15T00:00:00.000Z"

    result = build_close_sprint_payload(name, start, end)

    expected = {
        "state": "closed",
        "name": name,
        "startDate": start,
        "endDate": end
    }

    assert result == expected
