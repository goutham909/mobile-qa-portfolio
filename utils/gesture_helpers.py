"""W3C touch gestures with coordinates expressed as fractions of the screen,
so the same call works on any resolution."""

from __future__ import annotations

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from utils.wait_helpers import Locator, Waits


class Gestures:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.waits = Waits(driver)

    def _point(self, x_pct: float, y_pct: float) -> tuple[int, int]:
        size = self.driver.get_window_size()
        return int(size["width"] * x_pct), int(size["height"] * y_pct)

    def _builder(self, duration_ms: int) -> ActionBuilder:
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        return ActionBuilder(self.driver, mouse=finger, duration=duration_ms)

    def swipe(self, start: tuple[float, float], end: tuple[float, float], duration_ms: int = 600) -> None:
        """Swipe between two points given as (x, y) screen fractions in [0, 1]."""
        x1, y1 = self._point(*start)
        x2, y2 = self._point(*end)
        actions = self._builder(duration_ms)
        actions.pointer_action.move_to_location(x1, y1)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(x2, y2)
        actions.pointer_action.release()
        actions.perform()

    def scroll_down(self, distance: float = 0.5) -> None:
        """Reveal content further down the page (finger moves up)."""
        top = 0.5 - distance / 2
        self.swipe((0.5, 1 - top), (0.5, top))

    def scroll_up(self, distance: float = 0.5) -> None:
        top = 0.5 - distance / 2
        self.swipe((0.5, top), (0.5, 1 - top))

    def pull_to_refresh(self) -> None:
        self.swipe((0.5, 0.25), (0.5, 0.75), duration_ms=800)

    def long_press(self, element: WebElement, duration_ms: int = 1000) -> None:
        rect = element.rect
        x = rect["x"] + rect["width"] // 2
        y = rect["y"] + rect["height"] // 2
        actions = self._builder(250)
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration_ms / 1000)
        actions.pointer_action.release()
        actions.perform()

    def scroll_to(self, locator: Locator, max_swipes: int = 6) -> WebElement:
        """Scroll down until the locator is visible. Stops early when the page stops moving."""
        previous_source = None
        for _ in range(max_swipes + 1):
            if self.waits.is_visible(locator, timeout=1):
                return self.waits.visible(locator)
            source = self.driver.page_source
            if source == previous_source:
                break
            previous_source = source
            self.scroll_down()
        raise NoSuchElementException(f"{locator} not found after scrolling")

    def android_scroll(self, direction: str = "down", percent: float = 0.75) -> bool:
        """Native UiAutomator2 scroll. Returns True while more content can be scrolled."""
        size = self.driver.get_window_size()
        return bool(
            self.driver.execute_script(
                "mobile: scrollGesture",
                {
                    "left": int(size["width"] * 0.1),
                    "top": int(size["height"] * 0.2),
                    "width": int(size["width"] * 0.8),
                    "height": int(size["height"] * 0.6),
                    "direction": direction,
                    "percent": percent,
                },
            )
        )
