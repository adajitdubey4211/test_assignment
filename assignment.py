from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# Setting up WebDriver
driver = webdriver.Chrome() 

# Opening the website
driver.get("https://www.saucedemo.com/")


## task 1
# Login with valid credentials
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
# Verifying successful login
assert "inventory.html" in driver.current_url, "Login failed"


## task 2
# Selecting filter from "Price (low to high)"
driver.find_element(By.CLASS_NAME, "product_sort_container").send_keys("Price (low to high)")
# Adding items into cart
driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
# Verifying cart count
cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
assert cart_count == "2", "Cart count is incorrect"
print("✅ Items added to cart successfully.")


## task 3
# Click on product to open details page
driver.find_element(By.LINK_TEXT, "Sauce Labs Onesie").click()
# Adding item to cart
driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
# Verifying cart count
cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
assert cart_count == "3", "Cart count is incorrect"



## task 4
# Opening cart page
driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
# Removing item (assuming "Sauce Labs Onesie" is within $8-$10)
driver.find_element(By.ID, "remove-sauce-labs-onesie").click()
# Verifying cart count 
cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
assert cart_count == "2", "Cart count did not update correctly"



## task 5
# Click checkout
driver.find_element(By.ID, "checkout").click()
# Filling out checkout form
driver.find_element(By.ID, "first-name").send_keys("Ajit")
driver.find_element(By.ID, "last-name").send_keys("Dubey")
driver.find_element(By.ID, "postal-code").send_keys("123456")
# Continue to overview page
driver.find_element(By.ID, "continue").click()
# Print total price
total_price = driver.find_element(By.CLASS_NAME, "summary_total_label").text
print("Total Amount:", total_price)
# Finish purchase
driver.find_element(By.ID, "finish").click()
# Verify order completion
success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
assert success_message == "THANK YOU FOR YOUR ORDER", "Order not completed"


## task 6
# Open menu and logout
driver.find_element(By.ID, "react-burger-menu-btn").click()
driver.find_element(By.ID, "logout_sidebar_link").click()
# Verify redirection to login page
assert "saucedemo.com" in driver.current_url, "Logout failed"
print("✅ Successfully logged out.")


# Logout and close the browser
time.sleep(20)
driver.quit()
