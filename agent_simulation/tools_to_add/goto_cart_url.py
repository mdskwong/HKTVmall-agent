def goto_cart_url(url):
    """
    Go to the cart page.
    
    Args:
        url(str): the target url of cart page
        
    Returns:
    None
    """
    try:
        from selenium_utils.reconnect_driver import reconnect_driver
        driver = reconnect_driver()
        driver.get(url)
        print(f"[{(__name__)}]: successfully go to url: {url}")
    
    except Exception as e:
        print(f"[{(__name__)}]: {e}")

