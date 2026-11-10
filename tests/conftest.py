"""Shared fixtures plus failure evidence (screenshot + UI hierarchy) for every failed test."""

from __future__ import annotations

import re
from collections.abc import Iterator

import pytest
from selenium.common.exceptions import WebDriverException

from config.config import Config
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory

EVIDENCE_DIR = Config.REPORTS_DIR / "failures"


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> Iterator:
    drv = DriverFactory.create()
    yield drv
    call_report = getattr(request.node, "rep_call", None)
    DriverFactory.quit(drv, passed=call_report.passed if call_report else None)


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver).open()


@pytest.fixture
def catalog(login_page: LoginPage) -> InventoryPage:
    """Start from the catalog with the standard user already signed in."""
    return login_page.login_as(Config.STANDARD_USER)


@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report) -> None:
    report.title = f"My Demo App - {Config.PLATFORM.title()} ({Config.RUN_ON})"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when not in ("setup", "call") or not report.failed:
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^\w.-]+", "_", item.nodeid)
    try:
        screenshot_b64 = drv.get_screenshot_as_base64()
        drv.get_screenshot_as_file(str(EVIDENCE_DIR / f"{stem}.png"))
        (EVIDENCE_DIR / f"{stem}.xml").write_text(drv.page_source, encoding="utf-8")
    except WebDriverException:
        return

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html:
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(screenshot_b64, name="Screen at failure"))
        report.extras = extras
