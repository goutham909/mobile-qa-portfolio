"""Authentication: happy path plus the negative cases that matter to a real release."""

import pytest

from config.config import Config
from pages.login_page import LoginPage

STANDARD = Config.STANDARD_USER
LOCKED = Config.LOCKED_USER


@pytest.mark.smoke
def test_valid_login_lands_on_catalog(login_page: LoginPage):
    catalog = login_page.login_as(STANDARD)

    assert catalog.is_loaded(), "Catalog was not shown after a valid login"
    assert catalog.product_titles(), "Catalog loaded without any products"


@pytest.mark.regression
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param(LOCKED.username, LOCKED.password, LoginPage.LOCKED_OUT_MSG, id="locked-out-user"),
        pytest.param("", STANDARD.password, LoginPage.USERNAME_REQUIRED_MSG, id="empty-username"),
        pytest.param(STANDARD.username, "", LoginPage.PASSWORD_REQUIRED_MSG, id="empty-password"),
        pytest.param(STANDARD.username, "wrong-pass", LoginPage.INVALID_CREDENTIALS_MSG, id="wrong-password"),
        pytest.param("nobody@example.com", STANDARD.password, LoginPage.INVALID_CREDENTIALS_MSG, id="unknown-user"),
    ],
)
def test_invalid_login_is_rejected(login_page: LoginPage, username: str, password: str, expected_error: str):
    login_page.submit(username, password)

    assert login_page.has_error(expected_error), f"Expected error {expected_error!r} was not shown"
    assert login_page.is_open(), "User left the login screen despite invalid credentials"
