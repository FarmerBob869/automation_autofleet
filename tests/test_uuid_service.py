import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = "https://qatask.netlify.app/"

@pytest.fixture(scope="module")
def driver():
    """Set up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    yield driver
    driver.quit()

def test_generate_uuid(driver):
    """Test the Generate button generates a UUID."""
    generate_button = driver.find_element(By.ID, 'generate')
    generate_button.click()
    uuid_element = driver.find_element(By.ID, 'uuid-display')
    assert uuid_element.text != "", "UUID was not generated!"

def test_clear_uuid(driver):
    """Test the Clear button removes the UUID."""
    clear_button = driver.find_element(By.ID, 'clear')
    clear_button.click()
    uuid_element = driver.find_element(By.ID, 'uuid-display')
    assert uuid_element.text == "", "UUID was not cleared!"

def test_copy_uuid(driver):
    """Test the Copy button copies the UUID to clipboard."""
    generate_button = driver.find_element(By.ID, 'generate')
    generate_button.click()
    copy_button = driver.find_element(By.ID, 'copy')
    uuid_element = driver.find_element(By.ID, 'uuid-display')
    uuid = uuid_element.text

    copy_button.click()
    driver.execute_script("document.querySelector('#uuid-display').focus()")
    clipboard_content = driver.execute_script("return navigator.clipboard.readText()")
    assert clipboard_content == uuid, "Copied UUID does not match!"
