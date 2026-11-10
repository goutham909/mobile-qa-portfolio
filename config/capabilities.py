"""Appium capability builders for Android (UiAutomator2) and iOS (XCUITest)."""

from __future__ import annotations

from pathlib import Path

from appium.options.android import UiAutomator2Options
from appium.options.common import AppiumOptions
from appium.options.ios import XCUITestOptions

from config.config import Config


def _app_reference() -> str | None:
    """Return the app to install, or None to launch an already-installed build."""
    app = Config.APP_PATH
    if not app:
        return None
    if Config.RUN_ON == "saucelabs" or app.startswith(("storage:", "http://", "https://")):
        return app
    return app if Path(app).exists() else None


def _sauce_options() -> dict:
    return {
        "username": Config.SAUCE_USERNAME,
        "accessKey": Config.SAUCE_ACCESS_KEY,
        "build": Config.BUILD_NAME,
        "name": f"My Demo App - {Config.PLATFORM}",
        "appiumVersion": "latest",
    }


def android_options() -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.device_name = Config.DEVICE_NAME
    if Config.PLATFORM_VERSION:
        options.platform_version = Config.PLATFORM_VERSION
    if Config.UDID:
        options.udid = Config.UDID

    app = _app_reference()
    if app:
        options.app = app
    options.app_package = Config.ANDROID_PACKAGE
    options.app_activity = Config.ANDROID_ACTIVITY
    options.app_wait_activity = "*"

    options.auto_grant_permissions = True
    options.new_command_timeout = Config.NEW_COMMAND_TIMEOUT
    options.no_reset = False
    options.set_capability("appium:disableWindowAnimation", True)
    return options


def ios_options() -> XCUITestOptions:
    options = XCUITestOptions()
    options.device_name = Config.DEVICE_NAME
    if Config.PLATFORM_VERSION:
        options.platform_version = Config.PLATFORM_VERSION
    if Config.UDID:
        options.udid = Config.UDID

    app = _app_reference()
    if app:
        options.app = app
    else:
        options.bundle_id = Config.IOS_BUNDLE_ID

    options.new_command_timeout = Config.NEW_COMMAND_TIMEOUT
    options.no_reset = False
    options.set_capability("appium:autoAcceptAlerts", True)
    return options


def build_options() -> AppiumOptions:
    options = android_options() if Config.PLATFORM == "android" else ios_options()
    if Config.RUN_ON == "saucelabs":
        options.set_capability("sauce:options", _sauce_options())
    return options
