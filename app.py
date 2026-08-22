import runpy
import sys
from pathlib import Path

ui_directory = Path(__file__).resolve().parent / "ui"
sys.path.insert(0, str(ui_directory))
runpy.run_path(str(ui_directory / "app.py"), run_name="__main__")
