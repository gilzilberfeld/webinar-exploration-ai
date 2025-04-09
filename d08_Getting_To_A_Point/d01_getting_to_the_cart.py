from playwright.sync_api import sync_playwright



def add_items_to_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the login page
        page.goto("https://www.saucedemo.com/v1/index.html")

        # Login with valid credentials
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        # Verify we're on the products page
        assert "inventory.html" in page.url, "Login failed"
        print("Successfully logged in")

        # Add first item to cart
        first_add_button = page.locator(".inventory_item:nth-child(1) button.btn_primary")
        first_item_name = page.locator(".inventory_item:nth-child(1) .inventory_item_name").text_content()
        first_add_button.click()
        print(f"Added item 1: {first_item_name}")

        # Add second item to cart
        second_add_button = page.locator(".inventory_item:nth-child(4) button.btn_primary")
        second_item_name = page.locator(".inventory_item:nth-child(4) .inventory_item_name").text_content()
        second_add_button.click()
        print(f"Added item 2: {second_item_name}")

        # Verify cart count is 2
        cart_badge = page.locator(".shopping_cart_badge")
        assert cart_badge.text_content() == "2", "Cart count incorrect"
        print("Cart count verified as 2")

        # Navigate to cart page
        page.click(".shopping_cart_link")
        assert "cart.html" in page.url, "Failed to navigate to cart page"
        print("Successfully navigated to cart page")

        # Keep the browser open for manual exploration
        print("\nBrowser is open for you to continue testing manually.")
        print("The script has completed the requested steps.")

        # Wait for user to close browser manually
        input("Press Enter to close the browser when you're finished testing...")
        browser.close()


if __name__ == "__main__":
    add_items_to_cart()