import logging
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def reset_root_handlers():
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)


if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
