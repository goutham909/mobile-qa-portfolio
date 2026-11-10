"""Explicit-wait helpers. The framework never calls time.sleep()."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config

Locator = tuple[str, str]
T = TypeVar("T")


class Waits:
    def __init__(self, driver: WebDriver, timeout: float = Config.EXPLICIT_WAIT, poll: float = 0.25):
        self.driver = driver
        self.timeout = timeout
        self.poll = poll

    def _wait(self, timeout: float | None = None) -> WebDriverWait:
        return WebDriverWait(
            self.driver,
            timeout if timeout is not None else self.timeout,
            poll_frequency=self.poll,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def until(self, condition: Callable[[WebDriver], T], timeout: float | None = None, message: str = "") -> T:
        return self._wait(timeout).until(condition, message)

    def visible(self, locator: Locator, timeout: float | None = None) -> WebElement:
        return self.until(EC.visibility_of_element_located(locator), timeout, f"Not visible: {locator}")

    def clickable(self, locator: Locator, timeout: float | None = None) -> WebElement:
        return self.until(EC.element_to_be_clickable(locator), timeout, f"Not clickable: {locator}")

    def present(self, locator: Locator, timeout: float | None = None) -> WebElement:
        return self.until(EC.presence_of_element_located(locator), timeout, f"Not present: {locator}")

    def all_present(self, locator: Locator, timeout: float | None = None) -> list[WebElement]:
        return self.until(EC.presence_of_all_elements_located(locator), timeout, f"None present: {locator}")

    def invisible(self, locator: Locator, timeout: float | None = None) -> bool:
        return bool(self.until(EC.invisibility_of_element_located(locator), timeout, f"Still visible: {locator}"))

    def text_contains(self, locator: Locator, text: str, timeout: float | None = None) -> bool:
        return self.until(
            EC.text_to_be_present_in_element(locator, text), timeout, f"Text {text!r} not in {locator}"
        )

    def is_visible(self, locator: Locator, timeout: float = Config.SHORT_WAIT) -> bool:
        """Non-throwing visibility check for assertions and branching."""
        try:
            self.visible(locator, timeout)
            return True
        except TimeoutException:
            return False
