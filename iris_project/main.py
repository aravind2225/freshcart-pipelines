import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


PROJECT_PATH = Path(__file__).resolve().parent
MAGE_URL = "http://localhost:6789"
STARTUP_TIMEOUT_SECONDS = 60


def _mage_executable() -> str:
    executable_name = "mage.exe" if os.name == "nt" else "mage"
    executable = Path(sys.executable).resolve().with_name(executable_name)
    if executable.is_file():
        return str(executable)

    executable = shutil.which("mage")
    if executable is None:
        raise FileNotFoundError(
            "Mage CLI was not found. Install the project requirements and try again."
        )
    return executable


def _mage_is_available() -> bool:
    try:
        with urllib.request.urlopen(MAGE_URL, timeout=1) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def _wait_for_mage(process: subprocess.Popen) -> None:
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                f"Mage exited during startup with status {process.returncode}."
            )
        if _mage_is_available():
            return
        time.sleep(0.5)

    if process.poll() is None:
        process.terminate()
    raise TimeoutError(
        f"Mage did not become available at {MAGE_URL} "
        f"within {STARTUP_TIMEOUT_SECONDS} seconds."
    )


def main() -> None:
    if not _mage_is_available():
        command = [
            _mage_executable(),
            "start",
            str(PROJECT_PATH),
            "--host",
            "localhost",
            "--port",
            "6789",
        ]
        process = subprocess.Popen(command, cwd=PROJECT_PATH)
        _wait_for_mage(process)

    if not webbrowser.open(MAGE_URL):
        print(f"Mage is running. Open {MAGE_URL} in your browser.")


if __name__ == "__main__":
    main()
