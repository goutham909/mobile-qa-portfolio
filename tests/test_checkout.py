"""Purchase journey: cart, shipping, payment, review, confirmation."""

import pytest

from pages.checkout_page import CheckoutPage, PaymentCard, ShippingAddress
from pages.inventory_page import InventoryPage

PRODUCT = "Sauce Labs Backpack"

ADDRESS = ShippingAddress(
    full_name="Goutham Kolla",
    address_line_1="221 Hitech City Road",
    city="Hyderabad",
    zip_code="500081",
    country="India",
)
CARD = PaymentCard(
    holder_name="Goutham Kolla",
    number="4111111111111111",
    expiry="03/30",
    security_code="123",
)


@pytest.mark.smoke
def test_end_to_end_purchase(catalog: InventoryPage):
    catalog.open_product(PRODUCT).add_to_cart()
    assert catalog.cart_count() == 1

    checkout = (
        catalog.open_cart()
        .proceed_to_checkout()
        .fill_shipping(ADDRESS)
        .to_payment()
        .fill_payment(CARD)
        .review_order()
        .place_order()
    )

    assert checkout.is_order_complete(), "Order confirmation screen was not shown"


@pytest.mark.regression
def test_cart_badge_tracks_quantity(catalog: InventoryPage):
    assert catalog.cart_count() == 0, "Cart should start empty for a fresh session"

    catalog.open_product(PRODUCT).add_to_cart(times=2)

    assert catalog.cart_count() == 2


@pytest.mark.regression
def test_shipping_requires_mandatory_fields(catalog: InventoryPage):
    checkout: CheckoutPage = catalog.open_product(PRODUCT).add_to_cart().open_cart().proceed_to_checkout()

    checkout.submit_empty_shipping()

    assert checkout.is_on_shipping(), "Empty shipping form should not advance to payment"
    missing = set(CheckoutPage.REQUIRED_FIELD_ERRORS) - set(checkout.visible_errors())
    assert not missing, f"Validation messages not shown: {sorted(missing)}"
