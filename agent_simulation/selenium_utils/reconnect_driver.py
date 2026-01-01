from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
def reconnect_driver():
    """
    Reconnection to the existing browser.

    Returns:
    driver
    """
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        time.sleep(2)
        print(f"[{__name__}]Reconnected to driver")
        return driver
    except Exception as e:
        print(f"[{__name__}] failed to reconnect to driver")
        return None