import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time

class SauceDemoTest:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 100)
        self.url = "https://www.saucedemo.com/"
        
    def setup(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def login(self, username, password):
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        
    def verify_login_error(self):
        error_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        assert "Epic sadface: Username and password do not match any user in this service" in error_message.text
        print("Login error verification successful")

    def sort_items(self):
        sort_dropdown = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_dropdown.select_by_value("lohi")
        
    def add_items_from_inventory(self):
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
        
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "2"
        print("Added items from inventory successfully")

    def add_item_from_product_page(self):
        # Click on the product to open details page
        product_link = self.wait.until(
            EC.element_to_be_clickable((By.ID, "item_2_title_link"))
        )
        product_link.click()

        # Wait for the "Add to Cart" button to appear and click it
        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_primary.btn_inventory"))
        )
        add_to_cart_button.click()

        # Verify cart count
        cart_badge = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert cart_badge.text == "3"
        print("Added item from product page successfully")

    def remove_item_from_cart(self):
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        
        for item in items:
            price_element = item.find_element(By.CLASS_NAME, "inventory_item_price")
            price = float(price_element.text.replace("$", ""))
            if 8 <= price <= 10:
                # Find the remove button within this specific cart item
                remove_button = item.find_element(By.CSS_SELECTOR, "button[id*='remove']")
                remove_button.click()
                break
                
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == "2"
        print("Removed item from cart successfully")

    def checkout_workflow(self):
        try:
            # Click on cart
            cart_link = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
            )
            cart_link.click()
        
            # Verify cart has items before proceeding
            cart_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name"))
            )
            if not cart_items:
                print("\nERROR: Cart is empty! Cannot proceed to checkout.")
                return False

            print("\nCart Items Before Checkout:")
            for item in cart_items:
                print(f"- {item.text}")

            # Click checkout button
            checkout_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "checkout"))
            )
            checkout_button.click()

            # Fill checkout form with explicit waits
            first_name = self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
            first_name.clear()
            first_name.send_keys("ajit")
            
            last_name = self.wait.until(EC.presence_of_element_located((By.ID, "last-name")))
            last_name.clear() 
            last_name.send_keys("dubey")
            
            postal = self.wait.until(EC.presence_of_element_located((By.ID, "postal-code")))
            postal.clear()
            postal.send_keys("125001")

            # Click continue with retry
            continue_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "continue")))
            continue_btn.click()

            # Verify items still present on checkout page
            checkout_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name"))
            )
            if not checkout_items:
                print("\nERROR: Items missing from checkout overview!")
                return False
                
            print("\nItems in Checkout Overview:")
            for item in checkout_items:
                print(f"- {item.text}")

            # Get and verify total amount
            total = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
            )
            if not total.text:
                print("\nERROR: Total amount not displayed!")
                return False
            print(f"\nTotal amount: {total.text}")

            # Complete checkout
            finish_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "finish")))
            finish_btn.click()

            # Verify success message
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
            )
            if "THANK YOU FOR YOUR ORDER" not in success_message.text:
                print("\nERROR: Order confirmation message not found!")
                return False
            print("\nCheckout completed successfully!")

            # Return to products
            back_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "back-to-products")))
            back_btn.click()
            
            return True

        except TimeoutException as te:
            print(f"\nCheckout failed - Timeout: Element not found or not clickable: {str(te)}")
            self.driver.save_screenshot("checkout_timeout_error.png")
            return False
            
        except Exception as e:
            print(f"\nCheckout failed - Unexpected error: {str(e)}")
            self.driver.save_screenshot("checkout_error.png")
            return False

    def logout(self):
        try:
            # Wait for burger menu and click
            menu_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
            )
            menu_button.click()
            
            # Wait for menu animation with explicit wait
            self.wait.until(
                EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
            )
            
            # Click logout
            logout_link = self.wait.until(
                EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
            )
            logout_link.click()
            
            # Verify redirect to login page
            self.wait.until(EC.url_to_be(self.url))
            assert self.driver.current_url == self.url
            print("\nLogout successful!")
            return True
            
        except TimeoutException as te:
            print(f"\nLogout failed - Timeout: {str(te)}")
            self.driver.save_screenshot("logout_timeout_error.png")
            return False
            
        except Exception as e:
            print(f"\nLogout failed - Unexpected error: {str(e)}")
            self.driver.save_screenshot("logout_error.png") 
            return False

    def run_tests(self):
        try:
            # Setup
            self.setup()
            time.sleep(2)
            
            # Test 1: Valid Login
            self.login("standard_user", "secret_sauce")
            assert "/inventory.html" in self.driver.current_url
            print("Valid login successful")
            time.sleep(2)
            
            # Test 2: Sort and Add Items
            self.sort_items()
            self.add_items_from_inventory()
            time.sleep(2)
            
            # Test 3: Add Item from Product Page
            self.add_item_from_product_page()
            time.sleep(2)                                                
            
            # Test 4: Remove Item
            self.remove_item_from_cart()
            time.sleep(2)
            
            # Test 5: Checkout
            self.checkout_workflow()
            time.sleep(2)
            
            # Test 6: Logout
            self.logout()
            time.sleep(2)
            
            # Test 7: Invalid Login
            self.login("invalid_user", "wrong_password")
            self.verify_login_error()
            time.sleep(2)
        except Exception as e:
            print(f"Test failed: {str(e)}")
        finally:
            self.driver.quit()
             

if __name__ == "__main__":
    test = SauceDemoTest()
    test.run_tests()
