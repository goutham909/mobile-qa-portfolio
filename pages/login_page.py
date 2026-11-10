"""Login screen, reached from the side menu."""

from __future__ import annotations

from config.config import User
from pages.base_page import BasePage, a11y
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    MENU_BUTTON = a11y("open menu")
    MENU_LOGIN = a11y("menu item log in")
    SCREEN = a11y("login screen")
    USERNAME = a11y("Username input field")
    PASSWORD = a11y("Password input field")
    LOGIN_BUTTON = a11y("Login button")

    LOCKED_OUT_MSG = "Sorry, this user has been locked out."
    INVALID_CREDENTIALS_MSG = "Provided credentials do not match any user in this service."
    USERNAME_REQUIRED_MSG = "Username is required"
    PASSWORD_REQUIRED_MSG = "Password is required"

    def open(self) -> LoginPage:
        self.tap(self.MENU_BUTTON)
        self.tap(self.MENU_LOGIN)
        self.find(self.USERNAME)
        return self

    def is_open(self) -> bool:
        return self.is_displayed(self.USERNAME) and self.is_displayed(self.LOGIN_BUTTON)

    def submit(self, username: str, password: str) -> LoginPage:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.hide_keyboard()
        self.tap(self.LOGIN_BUTTON)
        return self

    def login_as(self, user: User) -> InventoryPage:
        self.submit(user.username, user.password)
        return InventoryPage(self.driver).wait_loaded()

    def has_error(self, message: str) -> bool:
        return self.is_displayed(self.by_text(message), timeout=5)
