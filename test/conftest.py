import sys
from pathlib import Path

# Inject project root so src becomes importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))