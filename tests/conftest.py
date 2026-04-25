import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.config import Config


def _wait_for_server(url, timeout=15):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


@pytest.fixture(scope="session", autouse=True)
def local_server():
    url = Config.BASE_URL.split("?")[0]

    if _wait_for_server(url, timeout=1):
        yield
        return

    project_root = Path(__file__).resolve().parents[1]
    dist_dir = project_root / "dist"
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        cwd=dist_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not _wait_for_server(url):
            raise RuntimeError("Local test server did not start")
        yield
    finally:
        server_process.terminate()
        server_process.wait(timeout=5)


@pytest.fixture
def driver():
    if Config.BROWSER.lower() != "chrome":
        raise ValueError(f"Unsupported browser: {Config.BROWSER}")

    options = ChromeOptions()
    options.set_capability("pageLoadStrategy", "normal")

    if os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    driver_instance = webdriver.Chrome(options=options)
    driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)

    yield driver_instance

    driver_instance.quit()
