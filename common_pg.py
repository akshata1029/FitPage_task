import time
from selenium.webdriver.support.ui import WebDriverWait

class CommonPage:
#common action page for all actions

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)  # wait

    def open_url(self, url):
       #open webpage
        self.driver.get(url)

    def zoom_out(self, zoom_percentage="100%"):
        #zoom out page
        self.driver.execute_script(f"document.body.style.zoom='{zoom_percentage}'")

    def find_element(self, locator_type, locator_value):
       #element - finds and return
        return self.driver.find_element(locator_type, locator_value)
