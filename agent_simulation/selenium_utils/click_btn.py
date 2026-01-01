from selenium_utils.reconnect_driver import reconnect_driver
from selenium.webdriver.common.by import By
import time 
def click_btn(driver, btn_class_name):
    """
    Click on the button with a specific btn_class_name.
    
    Args:
        btn_class_name(str): the class name of the button to be clicked on
        
    Returns:
    None
    """
    try:
        #driver = reconnect_driver()
        button = driver.find_element(By.CLASS_NAME, btn_class_name)
        button.click()
        time.sleep(2)
        print(f"[{(__name__)}]: clicked on button class: {btn_class_name}")
    
    except Exception as e:
        print(f"[{(__name__)}]: {e}")
