import logging
import sys
from pathlib import Path
from typing import cast
from unittest.mock import MagicMock

import pytest
from pydantic import HttpUrl

from src.models.board_config import BoardConfig


@pytest.fixture(autouse=True)
def reset_root_handlers():
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)


@pytest.fixture
def test_session() -> MagicMock:
    return MagicMock()


@pytest.fixture
def test_config() -> BoardConfig:
    return BoardConfig(
        base_url=cast(HttpUrl,'https://mock.net'),
        board_id=123,
        board_name='Test'
    )


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
