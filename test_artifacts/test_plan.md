# Test Plan: Sauce Labs My Demo App (iOS & Android)

| Field | Value |
| --- | --- |
| Document ID | TP-MDA-001 |
| Version | 1.0 |
| Prepared by | Goutham Kolla, Mobile QA & Test Automation Engineer |
| Application | Sauce Labs My Demo App, React Native build v1.3.x |
| Platforms | Android 11–15, iOS 16–18 |
| Status | Approved for execution |

## 1. Objective

Confirm that a shopper can sign in, browse the catalog, manage the cart and complete a purchase on both platforms. The release should hold up under real-world conditions: interrupts, poor networks, varied screen sizes and OS versions.

## 2. Scope

**In scope**
- Authentication: valid login, locked-out user, field validation, invalid credentials, logout
- Catalog: product list, sorting, product details, ratings, colour and quantity selection
- Cart: add, remove, update quantity, badge count, persistence across app restarts
- Checkout: shipping address, payment, review, order confirmation, required-field validation
- Non-functional: interrupt handling, network throttling and offline mode, orientation changes, accessibility labels, cold-start time

**Out of scope**
- Payment gateway integration (the demo app does not charge cards)
- Backend load or stress testing
- Web and desktop variants

## 3. Test approach

| Layer | Technique | Tooling | Owner |
| --- | --- | --- | --- |
| Smoke | Automated, run on every commit | Appium + pytest, GitHub Actions emulator | Automation |
| Regression | Automated, run nightly and before release | Appium + pytest on Sauce Labs real devices | Automation |
| Exploratory | Session-based, 60-minute charters | Real devices, screen recording, ADB logcat / Console.app | Manual |
| Interrupts and network | Scripted manual tests from BDD features | Android emulator console, Network Link Conditioner, Charles Proxy | Manual |
| Accessibility | TalkBack / VoiceOver walkthroughs, label audit | Accessibility Scanner, Xcode Accessibility Inspector | Manual |

**Automation design principles**
- Page Object Model; each test reads as a user journey.
- Accessibility-ID locators first, native text queries (UiAutomator / iOS predicate) second, and no brittle absolute XPath.
- Explicit waits only. No `time.sleep()` and no implicit waits.
- Failure evidence is collected automatically: a screenshot, the UI hierarchy XML and the Appium log.

## 4. Device and OS matrix

| Priority | Device | OS | Form factor | Execution |
| --- | --- | --- | --- | --- |
| P1 | Google Pixel 8 | Android 15 | 6.2" phone | Real device / cloud |
| P1 | Samsung Galaxy S23 | Android 14 (One UI) | 6.1" phone | Cloud |
| P1 | iPhone 15 | iOS 18 | 6.1" phone | Real device / cloud |
| P2 | Xiaomi Redmi Note 12 | Android 13 (MIUI) | 6.67" phone, low-mid tier | Cloud |
| P2 | iPhone SE (3rd gen) | iOS 17 | 4.7" small screen | Cloud |
| P2 | Samsung Galaxy Tab S9 | Android 14 | Tablet | Cloud |
| P3 | Pixel 6 emulator | Android 14 (API 34) | CI smoke | GitHub Actions |

## 5. Entry criteria
- The build is installable on all P1 devices and the smoke suite passes.
- Release notes and the list of changed features are available.
- Test data is available: `bob@example.com` (standard user) and `alice@example.com` (locked-out user).

## 6. Exit criteria
- 100% of P1 test cases executed, with at least 95% passing.
- No open Critical or High defects. Medium defects are triaged and accepted by the product owner.
- The automated regression suite is green on P1 devices, or every failure is linked to a known defect.
- The test summary report has been shared with stakeholders.

## 7. Defect management

| Severity | Definition | Target response |
| --- | --- | --- |
| Critical | Crash, data loss, or a blocked core journey (login, checkout) | Same day |
| High | Major feature broken, with a workaround | 2 days |
| Medium | Partial malfunction or a noticeable UI defect | Next sprint |
| Low | Cosmetic issue or copy error | Backlog |

Every defect includes environment details, numbered steps to reproduce, expected and actual results, and evidence (video, screenshots, logcat or device console). See [sample_bug_reports.md](sample_bug_reports.md).

## 8. Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| OEM skins (MIUI, One UI) change permission dialogs and keyboards | Flaky automation | Auto-grant permissions; keyboard-safe `hide_keyboard()`; OEM devices in the P2 matrix |
| Emulator timing differs from real devices | False passes in CI | Real-device regression on Sauce Labs before release |
| Locator changes in new builds | Broken tests | Accessibility IDs agreed with developers; centralised page objects |
| Network-dependent flows | Intermittent failures | Dedicated network-throttling suite; retry only at the infrastructure level (`--reruns 1`) |

## 9. Traceability

| Requirement | Test case | Type | Location |
| --- | --- | --- | --- |
| AUTH-01 Valid login | `test_valid_login_lands_on_catalog` | Automated, smoke | `tests/test_login.py` |
| AUTH-02 Locked user rejected | `test_invalid_login_is_rejected[locked-out-user]` | Automated, regression | `tests/test_login.py` |
| AUTH-03 Required fields | `test_invalid_login_is_rejected[empty-*]` | Automated, regression | `tests/test_login.py` |
| AUTH-04 Invalid credentials | `test_invalid_login_is_rejected[wrong-password, unknown-user]` | Automated, regression | `tests/test_login.py` |
| CART-01 Badge reflects quantity | `test_cart_badge_tracks_quantity` | Automated, regression | `tests/test_checkout.py` |
| CHK-01 End-to-end purchase | `test_end_to_end_purchase` | Automated, smoke | `tests/test_checkout.py` |
| CHK-02 Shipping validation | `test_shipping_requires_mandatory_fields` | Automated, regression | `tests/test_checkout.py` |
| NFR-01 Interrupt resilience | Interrupt scenarios | Manual / BDD | `bdd_features/interrupt_testing.feature` |
| NFR-02 Degraded network | Network scenarios | Manual / BDD | `bdd_features/network_throttling.feature` |

## 10. Deliverables
- This test plan
- Automated suite, with HTML reports produced on every CI run
- BDD feature files for manual and future automated execution
- Defect reports
- Test summary report, with a release recommendation of Go, Go with known issues, or No-Go
