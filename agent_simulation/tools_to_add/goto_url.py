def goto_url(url):
    """
    Go to a specific url in browser.
    
    Args:
        url(str): the target url to browse
        
    Returns:
    None
    """
    try:
        from selenium_utils.reconnect_driver import reconnect_driver
        from selenium_utils.click_btn import click_btn
        driver = reconnect_driver()
        driver.get(url)
        #To deal with ads
        click_btn(driver, btn_class_name = 'btnCloseLarge')
        print(f"[{(__name__)}]: successfully go to url: {url}")
    
    except Exception as e:
        print(f"[{(__name__)}]: {e}")

