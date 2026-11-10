"""Cart, shipping address, payment, review and order-complete screens."""

from __future__ import annotations

from dataclasses import dataclass

from pages.base_page import BasePage, a11y


@dataclass(frozen=True)
class ShippingAddress:
    full_name: str
    address_line_1: str
    city: str
    zip_code: str
    country: str


@dataclass(frozen=True)
class PaymentCard:
    holder_name: str
    number: str
    expiry: str  # MM/YY
    security_code: str


class CheckoutPage(BasePage):
    CART_SCREEN = a11y("cart screen")
    PROCEED_TO_CHECKOUT = a11y("Proceed To Checkout button")

    ADDRESS_SCREEN = a11y("checkout address screen")
    FULL_NAME = a11y("Full Name* input field")
    ADDRESS_LINE_1 = a11y("Address Line 1* input field")
    CITY = a11y("City* input field")
    ZIP_CODE = a11y("Zip Code* input field")
    COUNTRY = a11y("Country* input field")
    TO_PAYMENT = a11y("To Payment button")

    PAYMENT_SCREEN = a11y("checkout payment screen")
    CARD_HOLDER = a11y("Full Name* input field")
    CARD_NUMBER = a11y("Card Number* input field")
    EXPIRY = a11y("Expiration Date* input field")
    SECURITY_CODE = a11y("Security Code* input field")
    REVIEW_ORDER = a11y("Review Order button")

    REVIEW_SCREEN = a11y("checkout review order screen")
    PLACE_ORDER = a11y("Place Order button")

    COMPLETE_SCREEN = a11y("checkout complete screen")
    CONTINUE_SHOPPING = a11y("Continue Shopping button")

    REQUIRED_FIELD_ERRORS = (
        "Please provide your full name.",
        "Please provide your address.",
        "Please provide your city.",
        "Please provide your zip code.",
        "Please provide your country.",
    )

    def wait_for_cart(self) -> CheckoutPage:
        self.find(self.PROCEED_TO_CHECKOUT)
        return self

    def proceed_to_checkout(self) -> CheckoutPage:
        self.tap(self.PROCEED_TO_CHECKOUT)
        self.find(self.FULL_NAME)
        return self

    def fill_shipping(self, address: ShippingAddress) -> CheckoutPage:
        self.fill(self.FULL_NAME, address.full_name)
        self.fill(self.ADDRESS_LINE_1, address.address_line_1)
        self.fill(self.CITY, address.city)
        self.hide_keyboard()
        self.fill(self.ZIP_CODE, address.zip_code)
        self.fill(self.COUNTRY, address.country)
        self.hide_keyboard()
        return self

    def to_payment(self) -> CheckoutPage:
        self.scroll_to(self.TO_PAYMENT).click()
        self.find(self.CARD_NUMBER)
        return self

    def submit_empty_shipping(self) -> CheckoutPage:
        self.hide_keyboard()
        self.scroll_to(self.TO_PAYMENT).click()
        return self

    def is_on_shipping(self) -> bool:
        return self.is_displayed(self.TO_PAYMENT) or self.is_displayed(self.FULL_NAME)

    def fill_payment(self, card: PaymentCard) -> CheckoutPage:
        self.fill(self.CARD_HOLDER, card.holder_name)
        self.fill(self.CARD_NUMBER, card.number)
        self.hide_keyboard()
        self.fill(self.EXPIRY, card.expiry)
        self.fill(self.SECURITY_CODE, card.security_code)
        self.hide_keyboard()
        return self

    def review_order(self) -> CheckoutPage:
        self.scroll_to(self.REVIEW_ORDER).click()
        self.find(self.PLACE_ORDER)
        return self

    def place_order(self) -> CheckoutPage:
        self.scroll_to(self.PLACE_ORDER).click()
        return self

    def is_order_complete(self) -> bool:
        return self.is_displayed(self.COMPLETE_SCREEN, timeout=10)

    def visible_errors(self) -> list[str]:
        return [msg for msg in self.REQUIRED_FIELD_ERRORS if self.is_displayed(self.by_text(msg), timeout=1)]
