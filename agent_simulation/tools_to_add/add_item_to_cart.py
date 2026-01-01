def add_item_to_cart(product_code):
    """
    Add the item with the specified product code to the cart.
    
    Args:
        product_code(str): the product id to be added to cart
    
    Return:
    None
        
    """
    try:
        from selenium_utils.reconnect_driver import reconnect_driver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Reconnect to current broswer
        driver = reconnect_driver()
        product = driver.find_element(By.CSS_SELECTOR, f'div[data-id="{product_code}"]')
        add_to_cart_button = product.find_element(By.CLASS_NAME, "add-to-cart-button")

        # Wait for the button to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(add_to_cart_button))

        # Move to the button and click it
        driver.execute_script("arguments[0].click();", add_to_cart_button)
        
        print(f"[{__name__}]Successfully clicked Add to Cart for product code: {product_code}")
    except Exception as e:
        print(f"Error adding item to cart: {e}")
        
