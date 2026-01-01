from selenium_utils.reconnect_driver import reconnect_driver
from selenium_utils.click_btn import click_btn

#LLM first create empty brower
driver = reconnect_driver()

#Go to check out page
click_btn(driver, btn_class_name= "btn-cart")

