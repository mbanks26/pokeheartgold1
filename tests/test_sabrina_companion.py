"""Compatibility entry point for the revised engine-semantic tests."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("test_sabrina_stabilization.py")),run_name="__main__")
