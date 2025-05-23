from playwright.sync_api import Page, expect


def test_login_with_valid_credentials(page: Page):
    # Navigate to the login page
    page.goto("https://bstackdemo.com/signin")

    # Get the valid credentials displayed on the login page
    # For this test, we'll use the standard_user credentials
    username = "demouser"
    password = "testing123"

    # Fill in the login form
    page.fill("#user-name", username)
    page.fill("#password", password)

    # Click the login button
    page.click("#login-btn")

    # Verify successful navigation to the products page
    # Check if we're on the inventory page
    expect(page).to_have_url("https://bstackdemo.com/products")

    # Additional verification - check for elements that should be present on the products page
    expect(page.locator(".product_label")).to_be_visible()
    expect(page.locator(".inventory_item")).to_be_visible()

    print("Login test passed successfully!")
