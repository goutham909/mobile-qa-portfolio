"""Base class for all screens: element access, platform-aware locators, keyboard handling."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import WebDriverException

from config.config import Config
from utils.gesture_helpers import Gestures
from utils.wait_helpers import Locator, Waits


def a11y(accessibility_id: str) -> Locator:
    """Accessibility ID: content-desc on Android, accessibilityIdentifier/label on iOS."""
    return AppiumBy.ACCESSIBILITY_ID, accessibility_id


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.waits = Waits(driver)
        self.gestures = Gestures(driver)

    @property
    def is_android(self) -> bool:
        platform = str(self.driver.capabilities.get("platformName", Config.PLATFORM))
        return platform.lower() == "android"

    def platform_locator(self, android: Locator, ios: Locator) -> Locator:
        return android if self.is_android else ios

    def by_text(self, text: str) -> Locator:
        """Visible-text locator built on native engines (UiAutomator / iOS predicates), not XPath."""
        safe = text.replace("\\", "\\\\").replace('"', '\\"')
        return self.platform_locator(
            android=(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{safe}")'),
            ios=(AppiumBy.IOS_PREDICATE, f'label CONTAINS "{safe}" OR value CONTAINS "{safe}"'),
        )

    # Element access

    def find(self, locator: Locator, timeout: float | None = None) -> WebElement:
        return self.waits.visible(locator, timeout)

    def find_all(self, locator: Locator, timeout: float | None = None) -> list[WebElement]:
        return self.waits.all_present(locator, timeout)

    def tap(self, locator: Locator, timeout: float | None = None) -> None:
        self.waits.clickable(locator, timeout).click()

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        field = self.waits.clickable(locator)
        field.click()
        if clear:
            field.clear()
        if text:
            field.send_keys(text)

    def fill(self, locator: Locator, text: str) -> None:
        """Scroll the field into view, then type into it."""
        self.scroll_to(locator)
        self.type(locator, text)

    def get_text(self, locator: Locator) -> str:
        return self.find(locator).text

    def is_displayed(self, locator: Locator, timeout: float = Config.SHORT_WAIT) -> bool:
        return self.waits.is_visible(locator, timeout)

    def scroll_to(self, locator: Locator) -> WebElement:
        return self.gestures.scroll_to(locator)

    def hide_keyboard(self) -> None:
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except WebDriverException:
            # iOS keyboards without a dismiss key raise here; the flow continues either way.
            pass
