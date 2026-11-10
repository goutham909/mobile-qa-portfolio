# Sample Bug Reports

Prepared by: **Goutham Kolla**

These reports are written against the Sauce Labs My Demo App to show the reporting format and level of detail I deliver to clients. Evidence links are placeholders.

---

## BUG-001: Cart is emptied after the app is backgrounded during checkout

| Field | Value |
| --- | --- |
| Severity | High |
| Priority | P1 |
| Status | Open |
| Component | Checkout / state persistence |
| Environment | Samsung Galaxy S23, Android 14 (One UI 6.1), app v1.3.0 build 244, Wi-Fi |
| Reproducibility | 4 out of 5 attempts |

**Preconditions:** logged in as `bob@example.com`, with an empty cart.

**Steps to reproduce**
1. Open "Sauce Labs Backpack" and tap **Add To Cart**.
2. Tap the cart badge, then **Proceed To Checkout**.
3. Enter a full name and address.
4. Press the Home button and open three other apps, so the system is under memory pressure.
5. Wait about 2 minutes, then return to the app from Recents.

**Expected result:** the app resumes on the shipping screen with the entered data and the cart intact.

**Actual result:** the app cold-starts on the catalog. The cart badge is gone and the cart is empty.

**Impact:** shoppers who switch apps mid-checkout (for example to copy an address or read an OTP) lose their cart, which directly hurts conversion.

**Evidence:** `BUG-001_recording.mp4`, `BUG-001_logcat.txt` (process killed by `lmkd`; no saved-state restore)

**Suggested cause:** cart state is held only in memory; it should be persisted (for example with AsyncStorage) and rehydrated when the process restarts.

---

## BUG-002: "To Payment" button is hidden behind the keyboard on small screens

| Field | Value |
| --- | --- |
| Severity | Medium |
| Priority | P2 |
| Status | Open |
| Component | Checkout / layout |
| Environment | iPhone SE (3rd gen), iOS 17.5, app v1.3.0 build 162 |
| Reproducibility | Always |

**Steps to reproduce**
1. Add any product to the cart and proceed to the shipping address screen.
2. Tap **Zip Code** and type `500081`.
3. Try to reach the **To Payment** button.

**Expected result:** the form scrolls so the focused field and the primary action stay visible above the keyboard.

**Actual result:** the keyboard covers the button. The numeric keypad has no Return key, and scrolling is blocked while the keyboard is up, so the user has to tap blank space to dismiss it first.

**Evidence:** `BUG-002_iPhoneSE.png`, `BUG-002_recording.mp4`

---

## BUG-003: Duplicate order placed on a double-tap under a slow network

| Field | Value |
| --- | --- |
| Severity | Critical |
| Priority | P1 |
| Status | Open |
| Component | Checkout / order submission |
| Environment | Pixel 8, Android 15, network throttled to "3G Slow" (~400 kbps, 400 ms RTT) |
| Reproducibility | 3 out of 5 attempts |

**Steps to reproduce**
1. Throttle the network to slow 3G.
2. Complete shipping and payment and reach **Review Order**.
3. Tap **Place Order** twice in quick succession.

**Expected result:** the button is disabled after the first tap and exactly one order is created.

**Actual result:** two order requests are sent (visible in Charles Proxy) and the confirmation screen is shown twice.

**Evidence:** `BUG-003_charles_session.chls`, `BUG-003_recording.mp4`

**Suggested fix:** disable the button and show a loading state while the request is in flight, and add an idempotency key on the server.

---

## BUG-004: Product images have no accessibility label (TalkBack reads "unlabelled")

| Field | Value |
| --- | --- |
| Severity | Low |
| Priority | P3 |
| Status | Open |
| Component | Catalog / accessibility |
| Environment | Pixel 6 emulator, Android 14, TalkBack 14.1 |
| Reproducibility | Always |

**Steps to reproduce**
1. Turn on TalkBack.
2. Open the catalog and swipe through the items.

**Expected result:** each product image announces the product name, for example "Sauce Labs Backpack, image".

**Actual result:** TalkBack announces "unlabelled, image" for every product thumbnail.

**Standard:** WCAG 2.2 Success Criterion 1.1.1, Non-text Content (Level A).

**Evidence:** `BUG-004_accessibility_scanner.png`
