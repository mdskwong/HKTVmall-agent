from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():
    """
    Create a connection to the browser using selenium.

    Returns:
    driver
    """
    try:
        options = Options()
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("detach", True)  # Detach the browser
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        print(f"[{__name__}] Created driver at port=9222")
        return driver
    except Exception as e:
        print(f"[{__name__}] Failed to create driver at port=9222")
        raise 'something went wrong'