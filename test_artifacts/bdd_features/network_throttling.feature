@network @manual
Feature: Behaviour under degraded and changing network conditions
  As a shopper on an unreliable mobile network
  I want the app to stay responsive and tell me what is happening
  So that I never lose my cart or place an order twice

  Background:
    Given I am logged in as "bob@example.com"
    And network conditions are controlled with Network Link Conditioner (iOS) or the emulator network settings (Android)

  @P1 @android @ios
  Scenario Outline: Catalog loads within an acceptable time on throttled networks
    Given the network profile is "<profile>"
    When I open the catalog
    Then the product list is shown within <max_seconds> seconds
    And a loading indicator is shown until the content arrives
    And no product image stays broken once loading finishes

    Examples:
      | profile   | max_seconds |
      | Wi-Fi     | 2           |
      | LTE       | 3           |
      | 3G        | 6           |
      | Edge (2G) | 15          |

  @P1 @android @ios
  Scenario: Device goes offline while browsing
    Given I am on the catalog
    When I turn on airplane mode
    And I open "Sauce Labs Backpack"
    Then I see a clear message saying that I am offline
    And the app does not crash or freeze

  @P1 @android @ios
  Scenario: Order placement fails because the connection drops
    Given I am on the review order screen
    When the connection drops at the moment I tap "Place Order"
    Then I see an error with an option to retry
    And no order is created
    When the connection comes back and I tap "Retry"
    Then exactly one order is placed

  @P1 @android @ios
  Scenario: Double-tap on "Place Order" over a slow network
    Given the network profile is "3G"
    And I am on the review order screen
    When I tap "Place Order" twice in quick succession
    Then the button is disabled after the first tap
    And exactly one order request is sent

  @P2 @android @ios
  Scenario: Switching from Wi-Fi to cellular during checkout
    Given I am connected to Wi-Fi
    And I am filling in the payment form
    When Wi-Fi is turned off and the device falls back to cellular data
    Then the values I entered are still present
    And I can complete the order without logging in again

  @P2 @android @ios
  Scenario: High latency with packet loss
    Given the network has 1000 ms latency and 10% packet loss
    When I add "Sauce Labs Bike Light" to the cart
    Then the cart badge updates exactly once
    And the add-to-cart button gives feedback within 1 second

  @P2 @android @ios
  Scenario Outline: Request timeout handling
    Given the API responds after <delay> seconds
    When I log in
    Then I see "<outcome>"

    Examples:
      | delay | outcome                                   |
      | 2     | the catalog                               |
      | 20    | a loading indicator, then the catalog     |
      | 60    | a timeout error with an option to retry   |

  @P3 @android @ios
  Scenario: Captive-portal Wi-Fi (connected, but no internet access)
    Given I am connected to a Wi-Fi network that requires a captive-portal login
    When I open the catalog
    Then the app reports that there is no internet connection
    And it does not keep spinning without an error
