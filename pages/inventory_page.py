"""Product catalog, product details and the cart badge."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pages.base_page import BasePage, a11y
from pages.checkout_page import CheckoutPage


class InventoryPage(BasePage):
    SCREEN = a11y("products screen")
    STORE_ITEM = a11y("store item")
    ITEM_TITLE = a11y("store item text")
    SORT_BUTTON = a11y("sort button")
    SORT_OPTIONS = {
        "name_asc": a11y("nameAsc"),
        "name_desc": a11y("nameDesc"),
        "price_asc": a11y("priceAsc"),
        "price_desc": a11y("priceDesc"),
    }

    PRODUCT_SCREEN = a11y("product screen")
    ADD_TO_CART = a11y("Add To Cart button")
    CART_BADGE = a11y("cart badge")

    def wait_loaded(self) -> InventoryPage:
        self.find(self.SCREEN)
        self.find_all(self.STORE_ITEM)
        return self

    def is_loaded(self) -> bool:
        return self.is_displayed(self.SCREEN, timeout=10)

    def product_titles(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_TITLE)]

    def sort_by(self, option: str) -> InventoryPage:
        self.tap(self.SORT_BUTTON)
        self.tap(self.SORT_OPTIONS[option])
        return self.wait_loaded()

    def open_product(self, name: str) -> InventoryPage:
        self.scroll_to(self.by_text(name)).click()
        self.find(self.ADD_TO_CART)
        return self

    def add_to_cart(self, times: int = 1) -> InventoryPage:
        for _ in range(times):
            expected = self.cart_count() + 1
            self.tap(self.ADD_TO_CART)
            self.wait_for_cart_count(expected)
        return self

    def cart_count(self) -> int:
        if not self.is_displayed(self.CART_BADGE, timeout=1):
            return 0
        badge = self.find(self.CART_BADGE)
        child = self.platform_locator(
            android=(AppiumBy.CLASS_NAME, "android.widget.TextView"),
            ios=(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText"),
        )
        try:
            text = badge.find_element(*child).text
        except NoSuchElementException:
            return 0
        return int(text) if text.strip().isdigit() else 0

    def wait_for_cart_count(self, expected: int, timeout: float = 5) -> InventoryPage:
        try:
            self.waits.until(lambda _: self.cart_count() == expected, timeout)
        except TimeoutException as exc:
            raise AssertionError(f"Cart badge shows {self.cart_count()}, expected {expected}") from exc
        return self

    def open_cart(self) -> CheckoutPage:
        self.tap(self.CART_BADGE)
        return CheckoutPage(self.driver).wait_for_cart()
