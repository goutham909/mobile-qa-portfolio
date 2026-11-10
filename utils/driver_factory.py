"""Creates and tears down Appium sessions for local servers or Sauce Labs."""

from __future__ import annotations

import logging

from appium import webdriver
from selenium.common.exceptions import WebDriverException

from config.capabilities import build_options
from config.config import Config

log = logging.getLogger(__name__)


class DriverFactory:
    @staticmethod
    def create() -> webdriver.Remote:
        Config.validate()
        options = build_options()
        log.info("Starting %s session on %s (%s)", Config.PLATFORM, Config.RUN_ON, Config.server_url())
        driver = webdriver.Remote(command_executor=Config.server_url(), options=options)
        # Explicit waits only: implicit waits would silently stretch every negative check.
        driver.implicitly_wait(0)
        return driver

    @staticmethod
    def quit(driver: webdriver.Remote | None, passed: bool | None = None) -> None:
        if driver is None:
            return
        try:
            if Config.RUN_ON == "saucelabs" and passed is not None:
                driver.execute_script(f"sauce:job-result={'passed' if passed else 'failed'}")
            driver.quit()
        except WebDriverException as exc:
            log.warning("Driver did not quit cleanly: %s", exc)
