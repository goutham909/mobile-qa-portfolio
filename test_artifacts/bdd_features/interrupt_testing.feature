@interrupts @manual
Feature: App resilience to device interrupts
  As a shopper using My Demo App
  I want my session and cart to survive interruptions from the device
  So that I can finish a purchase without starting over

  Background:
    Given I am logged in as "bob@example.com"
    And I have "Sauce Labs Backpack" in my cart
    And I am on the checkout shipping address screen with the form partly filled in

  @P1 @android @ios
  Scenario: Incoming phone call during checkout
    When I receive an incoming phone call
    And I answer the call and talk for 30 seconds
    And I end the call
    Then the app returns to the shipping address screen
    And the values I entered are still present
    And my cart still contains 1 item

  @P1 @android @ios
  Scenario: Declined call shown as a heads-up notification
    When an incoming call appears as a heads-up notification
    And I decline the call
    Then the shipping address screen stays in the foreground
    And the field that had focus still has the keyboard open

  @P2 @android @ios
  Scenario: Incoming SMS notification is tapped and dismissed
    When I receive an SMS
    And I tap the notification to open the messaging app
    And I return to My Demo App using the Recents screen
    Then the app resumes on the shipping address screen without restarting

  @P1 @android @ios
  Scenario Outline: App is sent to the background for a period of time
    When I send the app to the background
    And I wait <duration>
    And I bring the app back to the foreground
    Then I see the "<expected_screen>" screen
    And my cart still contains 1 item

    Examples:
      | duration   | expected_screen          |
      | 5 seconds  | checkout shipping address |
      | 2 minutes  | checkout shipping address |
      | 30 minutes | checkout shipping address |

  @P1 @android
  Scenario: Android kills the process under memory pressure
    Given "Don't keep activities" is enabled in Developer options
    When I send the app to the background
    And I bring the app back to the foreground
    Then the app restores the shipping address screen
    And the values I entered are still present

  @P2 @android @ios
  Scenario: Screen orientation changes while the form is filled in
    When I rotate the device to landscape
    Then the shipping form is fully usable in landscape
    And the values I entered are still present
    When I rotate the device back to portrait
    Then the layout returns to portrait without overlapping elements

  @P2 @android @ios
  Scenario: Low-battery warning appears during checkout
    When the battery level drops to 15% and the system shows a low-battery dialog
    And I dismiss the dialog
    Then the checkout flow continues from where I left it

  @P2 @android @ios
  Scenario: Device is locked and unlocked
    When I lock the device
    And I unlock it after 1 minute
    Then the app is still on the shipping address screen
    And I am still logged in

  @P3 @android @ios
  Scenario: Alarm or timer goes off during order placement
    Given I am on the review order screen
    When an alarm goes off and I dismiss it
    And I tap "Place Order"
    Then exactly one order is placed
    And I see the checkout complete screen
