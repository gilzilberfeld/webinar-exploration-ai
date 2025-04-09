from playwright.sync_api import expect, Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/v1/index.html")
        return self

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return ProductsPage(self.page)


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_label = page.locator(".product_label")
        self.inventory_items = page.locator(".inventory_item")

    def is_displayed(self) -> bool:
        current_url = self.page.url
        return current_url == "https://www.saucedemo.com/v1/inventory.html"

    def has_products(self) -> bool:
        return self.inventory_items.count() > 0


def test_login_with_valid_credentials(page: Page):
    # Initialize page objects
    login_page = LoginPage(page)

    # Navigate to login page
    login_page.navigate()

    # Perform login with valid credentials
    products_page = login_page.login("standard_user", "secret_sauce")

    # Verify successful navigation to products page
    expect(products_page.is_displayed()).to_be_truthy()

    # Verify products are displayed
    expect(products_page.product_label).to_be_visible()
    expect(products_page.has_products()).to_be_truthy()

    print("Login test passed successfully!")