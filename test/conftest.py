import sys
from pathlib import Path

# Ensures the project root directory is on sys.path so that imports from the
# src folder work without needing a formal package install. Don't move this.

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))