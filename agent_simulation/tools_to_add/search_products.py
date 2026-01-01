def search_products(text):
    """
    Search products by locate the input text box, type the text, and click the search button.
    
    Args:
        text(str): the products to search
        
    Returns:
    None
    """

    try:
        from selenium_utils.reconnect_driver import reconnect_driver
        from selenium.webdriver.common.by import By
        from selenium_utils.click_btn import click_btn
        import time

        # Reconnect to current broswer
        driver = reconnect_driver()
        search_input = driver.find_element(By.CLASS_NAME, "SuggestionSearch-input")
        search_input.clear()  # Clear any existing text
        search_input.send_keys(text)  # Type the search text
        
        # Locate the search button by its class name and click it
        click_btn(driver, btn_class_name="SuggestionSearch-button")
        time.sleep(2)
        print(f"[{(__name__)}]: successfully searched: {text}")
        
    except Exception as e:
        print(f"[{(__name__)}]: Error occurred during the search: {e}")
        
