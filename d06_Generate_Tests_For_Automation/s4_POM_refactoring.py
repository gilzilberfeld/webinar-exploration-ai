import pytest
from playwright.sync_api import Page, expect
import re


class HomePage:
    """Page Object for the homepage with navigation functionality."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://ecommerce-playground.lambdatest.io/"

    def navigate(self):
        """Navigate to the homepage."""
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def click_my_account(self):
        """Click on My Account link using role/text/XPath priority."""
        # Role-based approach first
        try:
            my_account_link = self.page.get_by_role("link", name=re.compile(r"My Account|Account", re.IGNORECASE))
            if my_account_link.is_visible():
                my_account_link.click()
                return True
        except:
            pass

        # Text-based approach
        try:
            login_link = self.page.get_by_text("My Account", exact=False).first()
            if login_link.is_visible():
                login_link.click()
                return True
        except:
            pass

        # Alternative text patterns
        text_patterns = ["Login", "Sign In", "Account"]
        for pattern in text_patterns:
            try:
                link = self.page.get_by_text(pattern, exact=False).first()
                if link.is_visible():
                    link.click()
                    return True
            except:
                continue

        # XPath fallback
        try:
            xpath_link = self.page.locator(
                "xpath=//a[contains(@href,'account') or contains(text(),'Account') or contains(text(),'Login')]").first()
            if xpath_link.is_visible():
                xpath_link.click()
                return True
        except:
            pass

        return False

    def click_login_from_dropdown(self):
        """Click Login option from dropdown menu if present."""
        try:
            self.page.wait_for_timeout(1000)  # Wait for potential dropdown
            # Role-based approach
            dropdown_login = self.page.get_by_role("link", name="Login")
            if dropdown_login.is_visible():
                dropdown_login.click()
                return True
        except:
            pass

        # Text-based fallback
        try:
            dropdown_login = self.page.get_by_text("Login").filter(has=self.page.locator(".dropdown-menu")).first()
            if dropdown_login.is_visible():
                dropdown_login.click()
                return True
        except:
            pass

        return False


class LoginPage:
    """Page Object for the login page functionality."""

    def __init__(self, page: Page):
        self.page = page
        self.url = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"

    def navigate_directly(self):
        """Navigate directly to the login page."""
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def is_login_page(self):
        """Verify we're on the login page."""
        return "account/login" in self.page.url

    def is_returning_customer_section_visible(self):
        """Check if 'Returning Customer' section is visible."""
        try:
            returning_customer = self.page.get_by_text("Returning Customer", exact=False)
            return returning_customer.is_visible()
        except:
            return False

    def get_email_input(self):
        """Get email input field using role/text/XPath priority."""
        # Role-based approach
        try:
            email_input = self.page.get_by_role("textbox", name=re.compile(r"email|e-mail", re.IGNORECASE))
            if email_input.is_visible():
                return email_input
        except:
            pass

        # Text-based approach (label)
        try:
            email_input = self.page.get_by_label(re.compile(r"email|e-mail", re.IGNORECASE))
            if email_input.is_visible():
                return email_input
        except:
            pass

        # XPath fallback
        try:
            email_input = self.page.locator(
                "xpath=//input[@type='email' or @name='email' or contains(@placeholder,'mail')]").first()
            if email_input.is_visible():
                return email_input
        except:
            pass

        return None

    def get_password_input(self):
        """Get password input field using role/text/XPath priority."""
        # Role-based approach
        try:
            password_input = self.page.get_by_role("textbox", name=re.compile(r"password", re.IGNORECASE))
            if password_input.is_visible():
                return password_input
        except:
            pass

        # Text-based approach (label)
        try:
            password_input = self.page.get_by_label("Password", exact=False)
            if password_input.is_visible():
                return password_input
        except:
            pass

        # XPath fallback
        try:
            password_input = self.page.locator(
                "xpath=//input[@type='password' or @name='password' or contains(@placeholder,'assword')]").first()
            if password_input.is_visible():
                return password_input
        except:
            pass

        return None

    def get_login_button(self):
        """Get login button using role/text/XPath priority."""
        # Role-based approach
        try:
            login_button = self.page.get_by_role("button", name=re.compile(r"login|sign in", re.IGNORECASE))
            if login_button.is_visible():
                return login_button
        except:
            pass

        # Text-based approach
        try:
            login_button = self.page.get_by_text("Login", exact=False).filter(
                has=self.page.locator("button, input[type='submit']"))
            if login_button.is_visible():
                return login_button
        except:
            pass

        # XPath fallback
        try:
            login_button = self.page.locator(
                "xpath=//button[contains(text(),'Login')] | //input[@type='submit' and contains(@value,'Login')]").first()
            if login_button.is_visible():
                return login_button
        except:
            pass

        return None

    def fill_email(self, email: str):
        """Fill the email input field."""
        email_input = self.get_email_input()
        if email_input:
            email_input.fill(email)
            return True
        return False

    def fill_password(self, password: str):
        """Fill the password input field."""
        password_input = self.get_password_input()
        if password_input:
            password_input.fill(password)
            return True
        return False

    def click_login(self):
        """Click the login button."""
        login_button = self.get_login_button()
        if login_button:
            login_button.click()
            return True
        return False

    def login_with_credentials(self, email: str, password: str):
        """Complete login flow with provided credentials."""
        email_filled = self.fill_email(email)
        password_filled = self.fill_password(password)
        login_clicked = self.click_login()

        return email_filled and password_filled and login_clicked

    def get_error_message(self):
        """Get error message using role/text/XPath priority."""
        error_message = ""

        # Role-based approach for alerts
        try:
            alert_element = self.page.get_by_role("alert")
            if alert_element.is_visible():
                error_message = alert_element.text_content().strip()
                if error_message and len(error_message) > 5:
                    return error_message
        except:
            pass

        # Text-based approach for error messages
        error_text_patterns = [
            "Warning", "Error", "incorrect", "invalid",
            "wrong", "not match", "failed"
        ]

        for pattern in error_text_patterns:
            try:
                error_element = self.page.get_by_text(pattern, exact=False).first()
                if error_element.is_visible():
                    error_message = error_element.text_content().strip()
                    if error_message and len(error_message) > 5:
                        return error_message
            except:
                continue

        # XPath fallback for error messages
        try:
            xpath_error = self.page.locator(
                "xpath=//*[contains(@class,'alert') or contains(@class,'error') or contains(@class,'danger')][contains(text(),'Warning') or contains(text(),'Error') or contains(text(),'incorrect') or contains(text(),'invalid')]").first()
            if xpath_error.is_visible():
                error_message = xpath_error.text_content().strip()
                if error_message and len(error_message) > 5:
                    return error_message
        except:
            pass

        return None

    def has_error_message(self):
        """Check if any error message is displayed."""
        return self.get_error_message() is not None

    def wait_for_response(self):
        """Wait for page response after form submission."""
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

    def take_screenshot(self, filename: str):
        """Take a screenshot for debugging."""
        self.page.screenshot(path=filename)


class LoginTestActions:
    """High-level actions combining multiple page objects for login testing."""

    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)

    def navigate_to_login_from_homepage(self):
        """Complete navigation from homepage to login page."""
        # Navigate to homepage
        self.home_page.navigate()

        # Click My Account
        account_clicked = self.home_page.click_my_account()
        if not account_clicked:
            raise AssertionError("Could not find or click My Account link")

        # Handle dropdown if present
        self.home_page.click_login_from_dropdown()

        # Wait for login page to load
        self.login_page.wait_for_response()

        return self.login_page.is_login_page()

    def attempt_invalid_login(self, email: str = "invalid_user@nonexistent.com", password: str = "wrongpassword123"):
        """Attempt login with invalid credentials and return error information."""
        # Verify we can see the login form
        if not self.login_page.is_returning_customer_section_visible():
            raise AssertionError("Returning Customer section not visible")

        # Attempt login
        login_success = self.login_page.login_with_credentials(email, password)
        if not login_success:
            raise AssertionError("Could not complete login form submission")

        # Wait for response
        self.login_page.wait_for_response()

        return {
            "error_found": self.login_page.has_error_message(),
            "error_message": self.login_page.get_error_message(),
            "still_on_login_page": self.login_page.is_login_page()
        }


# Test Functions using Page Object Model

def test_login_invalid_credentials_error_display(page: Page):
    """
    Test that logging in with invalid credentials displays an appropriate error message.
    Uses Page Object Model with role/text/XPath priority.
    """

    # Initialize test actions
    login_test = LoginTestActions(page)

    # Navigate from homepage to login page
    on_login_page = login_test.navigate_to_login_from_homepage()
    assert on_login_page, f"Failed to navigate to login page. Current URL: {page.url}"

    # Verify login page elements
    expect(page).to_have_url(re.compile(r".*account/login.*"))
    expect(login_test.login_page.page.get_by_text("Returning Customer", exact=False)).to_be_visible()

    # Attempt invalid login
    result = login_test.attempt_invalid_login()

    # Verify error is displayed
    assert result["error_found"], "No error message found after login with invalid credentials"

    # Verify error message contains relevant keywords
    error_message = result["error_message"]
    error_message_lower = error_message.lower()
    relevant_keywords = [
        "warning", "error", "incorrect", "invalid", "wrong",
        "match", "credentials", "password", "email", "login"
    ]

    contains_relevant_keyword = any(keyword in error_message_lower for keyword in relevant_keywords)
    assert contains_relevant_keyword, f"Error message doesn't contain relevant keywords: '{error_message}'"

    # Verify user is still on login page
    assert result["still_on_login_page"], f"Should still be on login page after failed login"

    print(f"✓ Successfully verified error message for invalid login: '{error_message}'")


def test_login_invalid_credentials_alternative_approach(page: Page):
    """
    Alternative test approach using Page Object Model with enhanced debugging.
    """

    try:
        # Initialize page objects
        login_page = LoginPage(page)

        # Navigate directly to login page
        login_page.navigate_directly()
        login_page.take_screenshot("before_login_attempt.png")

        # Verify we can access form elements
        email_input = login_page.get_email_input()
        password_input = login_page.get_password_input()
        login_button = login_page.get_login_button()

        assert email_input is not None, "Email input not found"
        assert password_input is not None, "Password input not found"
        assert login_button is not None, "Login button not found"

        # Perform login with invalid credentials
        login_successful = login_page.login_with_credentials("test@invalid.com", "invalidpassword")
        assert login_successful, "Could not complete login form"

        # Wait for response and take screenshot
        login_page.wait_for_response()
        login_page.take_screenshot("after_login_attempt.png")

        # Check for error
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message found after invalid login attempt"

        # Ensure we didn't successfully log in
        assert "account/account" not in page.url, "Should not be logged in with invalid credentials"

        print(f"✓ Alternative approach: Error detected - '{error_message}'")

    except Exception as e:
        # Enhanced debugging
        LoginPage(page).take_screenshot("login_test_failure.png")
        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")
        raise e


# Pytest configuration
@pytest.fixture
def browser_context_args(browser_context_args):
    """Configure browser context for better test stability."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])