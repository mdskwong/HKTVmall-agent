from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
        options.add_argument('--window-size=1600,900')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(f"[{__name__}] Created driver at port=9222")
        return driver
    except Exception as e:
        print(f"[{__name__}] Failed to create driver at port=9222")
        raise 'something went wrong'