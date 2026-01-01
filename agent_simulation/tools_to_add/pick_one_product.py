def pick_one_product():
    """
    Pick the first product.
    
    Args:
    
    Return:
    Product code
    """

    try:
        from selenium_utils.reconnect_driver import reconnect_driver
        from selenium.webdriver.common.by import By
        from selenium_utils.json_products_data import load_results_from_json
        import time
        
        # Reconnect to current broswer
        driver = reconnect_driver()

        product_data = load_results_from_json()
        if product_data:
            result = product_data[0]['product_code']
        else:
            result = None

        print(f"[{(__name__)}]: Pick the first product with product_code {result}")
        return result
    except Exception as e:
        print(f"[{(__name__)}]:Unable to pick the first products: {e}")
        return None

