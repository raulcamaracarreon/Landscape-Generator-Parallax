# Language entry point: it
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from landscape_core import run

if __name__ == "__main__":
    run("it")
