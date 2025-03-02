import pytest
from selenium import webdriver
from login_pg import LoginPage

@pytest.fixture
def setup():
   #webdriver setup
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_success(setup):
    driver = setup
    login_page = LoginPage(driver)

    try:
        login_page.login("runningfitme1@gmail.com")
        print("Login Test PASSED")
    except Exception as e:
        print(f"Login Test FAILED: {e}")
        assert False, f"Test failed due to: {e}"

    assert "events/all" in driver.current_url, "Login failed: Did not reach Events page"
