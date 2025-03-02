import pytest
from selenium import webdriver
from login_pg import LoginPage
from event_pg import EventPage


@pytest.fixture(scope="class")
def setup():
    #intialize web
    driver = webdriver.Chrome()  # Ensure you have chromedriver installed
    driver.maximize_window()

    login_page = LoginPage(driver)
    login_page.login("fitmepageraaausnnning@gmail.com")  # Login first

    yield driver  # Provide driver to test functions

    driver.quit()  # Cleanup after test execution


@pytest.mark.usefixtures("setup")
class TestEventCreation:
    #Test Case for Creating an Event

    def test_create_event(self, setup):
        """Test if an event can be successfully created."""
        driver = setup
        event_page = EventPage(driver)

        event_page.open_event_page()
        event_page.click_create_event()
        event_page.fill_event_details(
            "Sample Event", "On-Ground", "2025-03-01", "2025-03-02",
            "Goa", "Miramar Beach", "South Goa", "Panaji", "Goa", "430001", "India"
        )

        # Assertion: Verify event is created by checking if redirected to event details page
        assert "events/all" in driver.current_url, " Event creation failed"
        print(" Event created successfully")
