from playwright.sync_api import Page, expect, sync_playwright

# ==============================================================================
# Page Object Model: Classes representing pages and components of the website.
# This makes the test script cleaner and easier to maintain.
# ==============================================================================

class HomePage:
    """
    Represents the home page and its interactions.
    """
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://ecommerce-playground.lambdatest.io/"
        # Locator for a product in the "Featured" section by its name
        self.product_link = lambda name: page.get_by_role("link", name=name, exact=True)

    def navigate(self):
        """Navigates to the home page."""
        print(f"Navigating to: {self.url}")
        self.page.goto(self.url)

    def select_product(self, product_name: str):
        """Clicks on a product from the home page to go to its detail page."""
        print(f"Selecting product: {product_name}")
        self.product_link(product_name).first.click()

class ProductPage:
    """
    Represents the product detail page and its interactions.
    """
    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_button = page.get_by_role("button", name="Add to Cart")
        self.success_alert = page.locator(".alert-success")

    def add_to_cart(self):
        """Clicks the 'Add to Cart' button."""
        print("Clicking 'Add to Cart' button...")
        self.add_to_cart_button.click()

    def verify_success_alert(self, product_name: str):
        """Waits for and verifies the success message after adding an item."""
        print(f"Verifying success alert for {product_name}...")
        # Check that the success alert is visible and contains the product name
        expect(self.success_alert).to_be_visible()
        expect(self.success_alert).to_contain_text(f"Success: You have added {product_name}")
        print("Success alert verified.")

class CartPage:
    """
    Represents the shopping cart page and its interactions.
    """
    def __init__(self, page: Page):
        self.page = page
        self.cart_heading = page.get_by_role("heading", name="Shopping Cart")

    def verify_on_page(self):
        """Verifies that the current page is the shopping cart page."""
        print("Verifying we are on the Shopping Cart page...")
        expect(self.cart_heading).to_be_visible()
        print("Successfully on the cart page.")

class TopNavigation:
    """
    Represents the main navigation bar at the top of the site.
    """
    def __init__(self, page: Page):
        self.page = page
        self.shopping_cart_link = page.get_by_role("link", name="Shopping Cart")

    def go_to_shopping_cart(self):
        """Navigates to the shopping cart page using the top link."""
        print("Navigating to the Shopping Cart page via top navigation...")
        self.shopping_cart_link.click()


# ==============================================================================
# Main test execution function
# ==============================================================================

def run(playwright: sync_playwright) -> None:
    """
    This script navigates to an e-commerce site, adds two items
    to the cart, and then navigates to the shopping cart page using POM.
    """
    # Launch the browser. Using Chromium, but can be 'firefox' or 'webkit'.
    # Headless is set to False to watch the script in action.
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    page = context.new_page()

    # Instantiate our page objects
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    top_nav = TopNavigation(page)

    # --- Test Steps ---

    # 1. Go to the home page
    home_page.navigate()

    # 2. Add the first item to the cart
    product1_name = "iPod Classic"
    home_page.select_product(product1_name)
    product_page.add_to_cart()
    product_page.verify_success_alert(product1_name)

    # 3. Go back to the home page to select another item
    home_page.navigate()

    # 4. Add the second item to the cart
    product2_name = "MacBook Pro"
    home_page.select_product(product2_name)
    product_page.add_to_cart()
    product_page.verify_success_alert(product2_name)

    # 5. Navigate to the shopping cart page
    top_nav.go_to_shopping_cart()
    cart_page.verify_on_page()

    print("\nThe script has paused. You can now inspect the browser. Close the browser to end.")

    # ---------------------
    # The script will pause here. You can add more actions below,
    # or simply close the browser window when you're done.
    # ---------------------

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
