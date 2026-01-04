import sys
from pathlib import Path

# Add the project root directory to Python path so `import src...` works
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))