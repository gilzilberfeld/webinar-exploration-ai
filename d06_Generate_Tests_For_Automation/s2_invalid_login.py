import pytest
from playwright.sync_api import Page, expect
import re


def test_login_invalid_credentials_error_display(page: Page):
    """
    Test that logging in with invalid credentials displays an appropriate error message.
    Uses role-based locators first, then text-based, then XPath as fallback.
    Starts from the main page and navigates to the login functionality.
    """

    # Navigate to the e-commerce playground homepage
    page.goto("https://ecommerce-playground.lambdatest.io/")
    page.wait_for_load_state("networkidle")

    # Find and click on "My Account" or "Login" link using roles and text
    login_clicked = False

    # Try role-based locators first
    try:
        my_account_link = page.get_by_role("link", name=re.compile(r"My Account|Account", re.IGNORECASE))
        if my_account_link.is_visible():
            my_account_link.click()
            login_clicked = True
    except:
        pass

    # Try text-based locators if role didn't work
    if not login_clicked:
        try:
            login_link = page.get_by_text("My Account", exact=False).first()
            if login_link.is_visible():
                login_link.click()
                login_clicked = True
        except:
            pass

    # Try alternative text patterns
    if not login_clicked:
        text_patterns = ["Login", "Sign In", "Account"]
        for pattern in text_patterns:
            try:
                link = page.get_by_text(pattern, exact=False).first()
                if link.is_visible():
                    link.click()
                    login_clicked = True
                    break
            except:
                continue

    # XPath fallback for login link
    if not login_clicked:
        try:
            xpath_link = page.locator(
                "xpath=//a[contains(@href,'account') or contains(text(),'Account') or contains(text(),'Login')]").first()
            if xpath_link.is_visible():
                xpath_link.click()
                login_clicked = True
        except:
            pass

    assert login_clicked, "Could not find login/My Account link on homepage"

    # Handle dropdown menu if it appears
    try:
        page.wait_for_timeout(1000)  # Wait for potential dropdown
        # Role-based approach for dropdown login option
        dropdown_login = page.get_by_role("link", name="Login")
        if dropdown_login.is_visible():
            dropdown_login.click()
    except:
        # Text-based fallback for dropdown
        try:
            dropdown_login = page.get_by_text("Login").filter(has=page.locator(".dropdown-menu")).first()
            if dropdown_login.is_visible():
                dropdown_login.click()
        except:
            pass

    # Wait for login page to load
    page.wait_for_load_state("networkidle")

    # Verify we're on the login page
    expect(page).to_have_url(re.compile(r".*account/login.*"))

    # Look for "Returning Customer" section using text
    returning_customer_heading = page.get_by_text("Returning Customer", exact=False)
    expect(returning_customer_heading).to_be_visible()

    # Find email input field using roles first
    email_input = None
    try:
        # Role-based approach - look for textbox with email-related name
        email_input = page.get_by_role("textbox", name=re.compile(r"email|e-mail", re.IGNORECASE))
        if not email_input.is_visible():
            email_input = None
    except:
        pass

    # Text-based approach for email field
    if email_input is None:
        try:
            email_input = page.get_by_label(re.compile(r"email|e-mail", re.IGNORECASE))
            if not email_input.is_visible():
                email_input = None
        except:
            pass

    # XPath fallback for email field
    if email_input is None:
        try:
            email_input = page.locator(
                "xpath=//input[@type='email' or @name='email' or contains(@placeholder,'mail')]").first()
        except:
            pass

    assert email_input is not None, "Email input field not found"

    # Find password input field using roles first
    password_input = None
    try:
        # Role-based approach for password field
        password_input = page.get_by_role("textbox", name=re.compile(r"password", re.IGNORECASE))
        if not password_input.is_visible():
            password_input = None
    except:
        pass

    # Text-based approach for password field
    if password_input is None:
        try:
            password_input = page.get_by_label("Password", exact=False)
            if not password_input.is_visible():
                password_input = None
        except:
            pass

    # XPath fallback for password field
    if password_input is None:
        try:
            password_input = page.locator(
                "xpath=//input[@type='password' or @name='password' or contains(@placeholder,'assword')]").first()
        except:
            pass

    assert password_input is not None, "Password input field not found"

    # Enter invalid credentials
    invalid_email = "invalid_user@nonexistent.com"
    invalid_password = "wrongpassword123"

    email_input.fill(invalid_email)
    password_input.fill(invalid_password)

    # Find and click the Login button using roles first
    login_button = None
    try:
        # Role-based approach for submit button
        login_button = page.get_by_role("button", name=re.compile(r"login|sign in", re.IGNORECASE))
        if not login_button.is_visible():
            login_button = None
    except:
        pass

    # Text-based approach for login button
    if login_button is None:
        try:
            login_button = page.get_by_text("Login", exact=False).filter(
                has=page.locator("button, input[type='submit']"))
            if not login_button.is_visible():
                login_button = None
        except:
            pass

    # XPath fallback for login button
    if login_button is None:
        try:
            login_button = page.locator(
                "xpath=//button[contains(text(),'Login')] | //input[@type='submit' and contains(@value,'Login')]").first()
        except:
            pass

    assert login_button is not None, "Login button not found"

    # Click login button
    login_button.click()

    # Wait for the response
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Additional wait for error message to appear

    # Look for error message using roles first
    error_found = False
    error_message = ""

    # Role-based approach for alerts
    try:
        alert_element = page.get_by_role("alert")
        if alert_element.is_visible():
            error_message = alert_element.text_content().strip()
            if error_message and len(error_message) > 5:
                error_found = True
                print(f"Error message found via role: '{error_message}'")
    except:
        pass

    # Text-based approach for error messages
    if not error_found:
        error_text_patterns = [
            "Warning", "Error", "incorrect", "invalid",
            "wrong", "not match", "failed"
        ]

        for pattern in error_text_patterns:
            try:
                error_element = page.get_by_text(pattern, exact=False).first()
                if error_element.is_visible():
                    error_message = error_element.text_content().strip()
                    if error_message and len(error_message) > 5:
                        error_found = True
                        print(f"Error message found via text: '{error_message}'")
                        break
            except:
                continue

    # XPath fallback for error messages
    if not error_found:
        try:
            xpath_error = page.locator(
                "xpath=//*[contains(@class,'alert') or contains(@class,'error') or contains(@class,'danger')][contains(text(),'Warning') or contains(text(),'Error') or contains(text(),'incorrect') or contains(text(),'invalid')]").first()
            if xpath_error.is_visible():
                error_message = xpath_error.text_content().strip()
                if error_message and len(error_message) > 5:
                    error_found = True
                    print(f"Error message found via XPath: '{error_message}'")
        except:
            pass

    # Verify that an error message is displayed
    assert error_found, f"No error message found after login with invalid credentials. Page content might need inspection."

    # Verify the error message contains relevant keywords
    error_message_lower = error_message.lower()
    relevant_keywords = [
        "warning", "error", "incorrect", "invalid", "wrong",
        "match", "credentials", "password", "email", "login"
    ]

    contains_relevant_keyword = any(keyword in error_message_lower for keyword in relevant_keywords)
    assert contains_relevant_keyword, f"Error message doesn't contain relevant keywords: '{error_message}'"

    # Verify we're still on the login page (not redirected to account page)
    current_url = page.url
    assert "account/login" in current_url, f"Should still be on login page, but current URL is: {current_url}"

    print(f"✓ Successfully verified error message for invalid login: '{error_message}'")


def test_login_invalid_credentials_alternative_approach(page: Page):
    """
    Alternative approach with role/text/XPath priority and enhanced debugging.
    """

    try:
        # Navigate to homepage
        page.goto("https://ecommerce-playground.lambdatest.io/")
        page.wait_for_load_state("networkidle")

        # Direct navigation to login page as fallback
        page.goto("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        page.wait_for_load_state("networkidle")

        # Take screenshot for debugging
        page.screenshot(path="before_login_attempt.png")

        # Fill email field - role first, then XPath
        email_filled = False
        try:
            email_field = page.get_by_role("textbox").filter(has=page.locator("[name='email'], [type='email']")).first()
            email_field.fill("test@invalid.com")
            email_filled = True
        except:
            try:
                email_field = page.locator("xpath=//input[@name='email' or @type='email']").first()
                email_field.fill("test@invalid.com")
                email_filled = True
            except:
                pass

        assert email_filled, "Could not fill email field"

        # Fill password field - role first, then XPath
        password_filled = False
        try:
            password_field = page.get_by_role("textbox").filter(has=page.locator("[type='password']")).first()
            password_field.fill("invalidpassword")
            password_filled = True
        except:
            try:
                password_field = page.locator("xpath=//input[@type='password']").first()
                password_field.fill("invalidpassword")
                password_filled = True
            except:
                pass

        assert password_filled, "Could not fill password field"

        # Submit the form - role first, then text, then XPath
        submitted = False
        try:
            submit_button = page.get_by_role("button", name=re.compile(r"login", re.IGNORECASE))
            submit_button.click()
            submitted = True
        except:
            try:
                submit_button = page.get_by_text("Login").filter(has=page.locator("button, input[type='submit']"))
                submit_button.click()
                submitted = True
            except:
                try:
                    submit_button = page.locator(
                        "xpath=//input[@type='submit'] | //button[contains(text(),'Login')]").first()
                    submit_button.click()
                    submitted = True
                except:
                    pass

        assert submitted, "Could not submit login form"

        # Wait for response
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Take screenshot after login attempt
        page.screenshot(path="after_login_attempt.png")

        # Check for error using role/text/XPath priority
        error_found = False

        # Role-based error detection
        try:
            alert = page.get_by_role("alert")
            if alert.is_visible():
                error_found = True
                print(f"Error found via role: {alert.text_content()}")
        except:
            pass

        # Text-based error detection
        if not error_found:
            try:
                warning_text = page.get_by_text("Warning", exact=False).first()
                if warning_text.is_visible():
                    error_found = True
                    print(f"Error found via text: {warning_text.text_content()}")
            except:
                pass

        # XPath error detection
        if not error_found:
            try:
                xpath_error = page.locator(
                    "xpath=//*[contains(@class,'alert-danger') or contains(@class,'error')]").first()
                if xpath_error.is_visible():
                    error_found = True
                    print(f"Error found via XPath: {xpath_error.text_content()}")
            except:
                pass

        assert error_found, "No error indicators found after invalid login"

        # Ensure we didn't successfully log in
        assert "account/account" not in page.url, "Should not be logged in with invalid credentials"

        print("✓ Alternative approach: Error detected for invalid login credentials")

    except Exception as e:
        # Take final screenshot for debugging
        page.screenshot(path="login_test_failure.png")
        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")
        raise e


# Pytest configuration and helper function
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