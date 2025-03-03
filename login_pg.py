from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common_pg import CommonPage  # Import the corrected CommonPage

class LoginPage(CommonPage):
    EMAIL_INPUT = (By.ID, "email")
    OTP_BUTTON = (By.XPATH, "(//button[normalize-space()='Get OTP'])[1]")
    VERIFY_OTP = (By.XPATH, "//button[normalize-space()='Verify OTP']")
    FIRSTNAME_INPUT = (By.XPATH, "//input[@id='firstName']")
    LASTNAME_INPUT = (By.XPATH, "//input[@id='lastName']")
    MOBILENUMBER_INPUT = (By.XPATH, "//input[@placeholder='Mobile number']")
    ORGANIZATION_INPUT = (By.XPATH, "//input[@id='organization-name']")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue']")
    EVENTS_PAGE_HEADER = (By.XPATH, "//div[@class='px-4 py-3 text-base font-medium text-center text-white rounded-lg cursor-pointer mt-11 bg-primary-500 hover:bg-primary-400']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 10)  

    def login(self, email):
        self.open_url("https://indiarunning-organizer-dashboard-staging.bombayrunning.com/")

        # Enter email
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.send_keys(email)

        # Click "Get OTP"
        otp_button = self.wait.until(EC.element_to_be_clickable(self.OTP_BUTTON))
        otp_button.click()

        # Enter OTP
        otp_values = "1234"  # Example OTP
        for i in range(4):
            otp_box = self.wait.until(EC.visibility_of_element_located((By.ID, f"otp{i}")))
            otp_box.send_keys(otp_values[i])

        # Click "Verify OTP"
        verify_otp = self.wait.until(EC.element_to_be_clickable(self.VERIFY_OTP))
        verify_otp.click()
        print("OTP verified")

        # Signup page actions
        firstname = self.wait.until(EC.visibility_of_element_located(self.FIRSTNAME_INPUT))
        firstname.send_keys("sakshi")
        lastname = self.wait.until(EC.visibility_of_element_located(self.LASTNAME_INPUT))
        lastname.send_keys("Singhh")
        mobilenumber = self.wait.until(EC.visibility_of_element_located(self.MOBILENUMBER_INPUT))
        mobilenumber.send_keys("9719839890")
        organizationname = self.wait.until(EC.visibility_of_element_located(self.ORGANIZATION_INPUT))
        organizationname.send_keys("Testing company1")

        # Locate Continue button
        continue_btn = self.wait.until(EC.presence_of_element_located(self.CONTINUE_BUTTON))

        # Scroll to the button before clicking
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
        time.sleep(1)

        # **Force click using JavaScript**
        self.driver.execute_script("arguments[0].click();", continue_btn)
        print("Successfully clicked Continue!")

        otp_values = "1234"  # Example OTP
        for i in range(4):
            otp_box = self.wait.until(EC.visibility_of_element_located((By.ID, f"otp{i}")))
            otp_box.send_keys(otp_values[i])

        # Click "Verify OTP"
        verify_otp = self.wait.until(EC.element_to_be_clickable(self.VERIFY_OTP))
        verify_otp.click()
        print("Mobile OTP verified")

        WebDriverWait(self.driver, 10).until(EC.url_contains("/events/all"))

        # Now check the current URL
        current_url = self.driver.current_url
        expected_url = "https://indiarunning-organizer-dashboard-staging.bombayrunning.com/events/all"

        if current_url == expected_url:
            print("Successfully redirected to Events page")
            events_page_header = self.wait.until(EC.visibility_of_element_located(self.EVENTS_PAGE_HEADER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", events_page_header)
        else:
            print("Redirection failed! Current URL:", current_url)


# Run script
if __name__ == "__main__":
    driver = webdriver.Chrome()  # Initialize WebDriver
    driver.maximize_window()

    login_page = LoginPage(driver)  # Pass driver to LoginPage
    login_page.login("runningfitme1@gmail.com")

    driver.quit()  # Close browser
