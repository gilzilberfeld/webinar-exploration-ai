from playwright.sync_api import sync_playwright



def add_items_to_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the login page
        page.goto("https://bstackdemo.com/signin")

        # Enter login credentials (replace with actual ones)
        page.fill("#username", "demouser")
        page.fill("#password", "testing123")

        # Click the login button
        page.click("#login-btn")

        # Wait for navigation to the product page
        page.wait_for_url("https://bstackdemo.com/products")

        # Select two items (adjust selectors based on actual HTML elements)
        page.click("button[data-testid='add-to-cart-0']")
        page.click("button[data-testid='add-to-cart-1']")

        # Navigate to the cart page
        page.click("#cart")

        # Wait for navigation to the cart page
        page.wait_for_url("https://bstackdemo.com/cart")
        print("Successfully navigated to cart page")

        # Keep the browser open for manual exploration
        print("\nBrowser is open for you to continue testing manually.")
        print("The script has completed the requested steps.")

        # Wait for user to close browser manually
        input("Press Enter to close the browser when you're finished testing...")
        browser.close()


if __name__ == "__main__":
    add_items_to_cart()