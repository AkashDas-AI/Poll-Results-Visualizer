"""Convenience runner script for Poll Results Visualizer.

Launches the Streamlit application using project-relative paths.
Author: Akash Das
"""

import sys
import subprocess
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent
    app_entry = project_root / "app" / "streamlit_app.py"

    if not app_entry.exists():
        print(f"Error: Application entry point not found at {app_entry}", file=sys.stderr)
        sys.exit(1)

    cmd = [sys.executable, "-m", "streamlit", "run", str(app_entry)]
    print(f"Launching Poll Results Visualizer from {project_root}...")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error launching application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
