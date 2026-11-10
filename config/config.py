"""Central runtime configuration.

Every value can be overridden with an environment variable (or a `.env` file at the
project root), so the same suite runs unchanged on a laptop, in CI, or on Sauce Labs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class User:
    username: str
    password: str


class Config:
    ROOT_DIR = ROOT_DIR
    REPORTS_DIR = ROOT_DIR / "reports"

    # Execution target
    PLATFORM = _env("PLATFORM", "android").lower()  # android | ios
    RUN_ON = _env("RUN_ON", "local").lower()  # local | saucelabs
    APPIUM_URL = _env("APPIUM_URL", "http://127.0.0.1:4723")

    # Device
    DEVICE_NAME = _env("DEVICE_NAME", "Android Emulator" if PLATFORM == "android" else "iPhone 15")
    PLATFORM_VERSION = _env("PLATFORM_VERSION")
    UDID = _env("UDID")

    # App under test: Sauce Labs "My Demo App" (React Native build).
    # Local runs take a file path; Sauce Labs runs take "storage:filename=<name>".
    APP_PATH = _env(
        "APP_PATH",
        str(ROOT_DIR / "apps" / ("my-demo-app.apk" if PLATFORM == "android" else "MyRNDemoApp.app")),
    )
    ANDROID_PACKAGE = "com.saucelabs.mydemoapp.rn"
    ANDROID_ACTIVITY = ".MainActivity"
    IOS_BUNDLE_ID = "com.saucelabs.mydemo.app.ios"

    # Timeouts (seconds)
    EXPLICIT_WAIT = int(_env("EXPLICIT_WAIT", "15"))
    SHORT_WAIT = int(_env("SHORT_WAIT", "3"))
    NEW_COMMAND_TIMEOUT = int(_env("NEW_COMMAND_TIMEOUT", "120"))

    # Sauce Labs
    SAUCE_USERNAME = _env("SAUCE_USERNAME")
    SAUCE_ACCESS_KEY = _env("SAUCE_ACCESS_KEY")
    SAUCE_REGION = _env("SAUCE_REGION", "eu-central-1")
    BUILD_NAME = _env("BUILD_NAME", "mobile-qa-portfolio-local")

    # Test data shipped with the demo app
    STANDARD_USER = User("bob@example.com", "10203040")
    LOCKED_USER = User("alice@example.com", "10203040")

    @classmethod
    def server_url(cls) -> str:
        if cls.RUN_ON == "saucelabs":
            return f"https://ondemand.{cls.SAUCE_REGION}.saucelabs.com:443/wd/hub"
        return cls.APPIUM_URL

    @classmethod
    def validate(cls) -> None:
        if cls.PLATFORM not in {"android", "ios"}:
            raise ValueError(f"PLATFORM must be 'android' or 'ios', got {cls.PLATFORM!r}")
        if cls.RUN_ON not in {"local", "saucelabs"}:
            raise ValueError(f"RUN_ON must be 'local' or 'saucelabs', got {cls.RUN_ON!r}")
        if cls.RUN_ON == "saucelabs" and not (cls.SAUCE_USERNAME and cls.SAUCE_ACCESS_KEY):
            raise ValueError("SAUCE_USERNAME and SAUCE_ACCESS_KEY are required when RUN_ON=saucelabs")
