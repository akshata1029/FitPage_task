from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from common_pg import CommonPage
from login_pg import LoginPage
from selenium.webdriver.common.keys import Keys


class EventPage(CommonPage):
    CREATE_EVENT_BTN = (By.XPATH, "//div[contains(text(),'Create Event')]")
    EVENT_NAME_INPUT = (By.XPATH, "//input[@id='Event Name_text']")
    EVENT_TYPE_RADIO_ONGROUND = (By.XPATH, "//input[@id='On-Ground']")
    EVENT_TYPE_RADIO_VIRTUAL = (By.XPATH, "//label[@for='Virtual']")
    EVENT_TYPE_RADIO_ONGROUND_VIRTUAL = (By.XPATH, "//input[@id='On-Ground+Virtual']")
    START_DATE_INPUT = (By.XPATH, "//input[@id='event_start_date']")
    END_DATE_INPUT = (By.XPATH, "//input[@id='event_end_date']")
    SAVE_BTN = (By.XPATH, "//span[@class='text-base font-normal']")
    LOCATION = (By.XPATH, "//input[@placeholder='Search location here']")
    ADDRESS = (By.XPATH, "//input[@id='Address_text']")
    AREA = (By.XPATH, "//input[@id='Area_text']")
    CITY = (By.XPATH, "//input[@id='City_text']")
    STATE = (By.XPATH, "//input[@id='State_text']")
    PINCODE = (By.XPATH, "//input[@id='PinCode']")
    COUNTRY = (By.XPATH, "//select[@id='country']")

    def __init__(self, driver):
        super().__init__(driver)  # Pass driver to CommonPage
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open_event_page(self):
        self.driver.get("https://indiarunning-organizer-dashboard-staging.bombayrunning.com/events/all")
        print("Opened event page")

    def click_create_event(self):
        """Handles clicking the 'Create Event' button, retrying if intercepted."""
        try:
            create_event_btn = self.wait.until(EC.element_to_be_clickable(self.CREATE_EVENT_BTN))
            create_event_btn.click()
            print("Clicked on 'Create Event' button")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException occurred. Retrying after scrolling...")
            self.driver.execute_script("arguments[0].scrollIntoView();", create_event_btn)
            time.sleep(1)  # Small wait before retrying
            create_event_btn.click()
            print("Clicked 'Create Event' after handling interception.")

    def select_event_type(self, event_type_element):
        """Selects event type while handling exceptions."""
        try:
            event_type_radio = self.wait.until(EC.element_to_be_clickable(event_type_element))
            event_type_radio.click()
            print("Selected event type.")
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException occurred. Retrying after scrolling...")
            self.driver.execute_script("arguments[0].scrollIntoView();", event_type_radio)
            time.sleep(1)
            event_type_radio.click()
            print("Selected event type after handling interception.")

    def set_date(self, date_input_element, date_value):
        """Set the date using send_keys for input type='date' fields"""
        try:
            date_input = self.wait.until(EC.element_to_be_clickable(date_input_element))
            date_input.clear()  # Clear any pre-filled date
            date_input.send_keys(date_value)  # Directly input the date (format: YYYY-MM-DD)
            print(f"Selected date: {date_value}")

        except Exception as e:
            print(f"Error setting date: {e}")

    def fill_event_details(self, event_name, event_type, start_date, end_date, location, address, area, city, state,
                           pincode, country):
        """Fills out event details in the form."""
        self.wait.until(EC.visibility_of_element_located(self.EVENT_NAME_INPUT)).send_keys(event_name)
        print(f"Entered event name: {event_name}")

        if event_type == "On-Ground":
            self.select_event_type(self.EVENT_TYPE_RADIO_ONGROUND)
        elif event_type == "Virtual":
            self.select_event_type(self.EVENT_TYPE_RADIO_VIRTUAL)
        elif event_type == "On-Ground+Virtual":
            self.select_event_type(self.EVENT_TYPE_RADIO_ONGROUND_VIRTUAL)

        self.set_date(self.START_DATE_INPUT, start_date)
        self.set_date(self.END_DATE_INPUT, end_date)

        self.wait.until(EC.visibility_of_element_located(self.LOCATION)).send_keys(location)
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS)).send_keys(address)
        self.wait.until(EC.visibility_of_element_located(self.AREA)).send_keys(area)
        self.wait.until(EC.visibility_of_element_located(self.CITY)).send_keys(city)
        self.wait.until(EC.visibility_of_element_located(self.STATE)).send_keys(state)
        self.wait.until(EC.visibility_of_element_located(self.PINCODE)).send_keys(pincode)
        self.wait.until(EC.visibility_of_element_located(self.COUNTRY)).send_keys(country)
        print("Event details filled successfully.")

        self.wait.until(EC.element_to_be_clickable(self.SAVE_BTN)).click()
        print("Clicked 'Save' button")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()

    login_page = LoginPage(driver)
    login_page.login("runningfitme@gmail.com")

    event_page = EventPage(driver)
    event_page.open_event_page()
    event_page.click_create_event()
    event_page.fill_event_details("Sample Event", "On-Ground", "2025-03-01", "2025-03-02", "Goa", "Miramar Beach",
                                  "South Goa", "Panaji", "Goa", "430001", "India")

    driver.quit()
