import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

URL = "https://qatask.netlify.app/"


#Create log for test results
def log_test_result(test_name, status, error_info=None):
    file_path = os.path.join(os.path.dirname(__file__), "testresult.txt")
    print(f"Logging result to {file_path}")
    with open(file_path, "a") as file:
        file.write(f"Test: {test_name}, Status: {status}\n")
        if error_info:
            file.write(f"Error Info: {error_info}\n")
    print(f"Logged result for {test_name}")

#Initialize the crome driver for local and git env.
@pytest.fixture(scope="module")
def driver():
    """Set up the Selenium WebDriver."""
    if os.getenv('GITHUB_ACTIONS'):
        # Running in GitHub Actions, use remote WebDriver
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
    else:
        # Running locally, use local chromedriver
        chromedriver_path = r"C:\Users\darwin\Documents\project\automation_autofleet\tests\chromedriver.exe"
        
        # Check if the file exists
        if not os.path.isfile(chromedriver_path):
            raise RuntimeError(f"chromedriver.exe not found at {chromedriver_path}")

        service = Service(executable_path=chromedriver_path)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(URL)
    yield driver
    driver.quit()
    
# Test case 1 UI: Test the page title and the presence of the <h1> element    
def test_page_title(driver):
    """Test the presence of the <h1> element and its text."""
    try:
        h1_element = driver.find_element(By.TAG_NAME, 'h1')
        assert h1_element.is_displayed(), log_test_result("test_page_title", "fail", f"<h1> element is not displayed!")
        assert h1_element.text == "UUID Generator", log_test_result("test_page_title", "fail", f"<h1> text is incorrect! Found: {h1_element.text}")
        log_test_result("test_page_title", "pass")
    except AssertionError as e:
        log_test_result("test_page_title", "fail", str(e))
        raise


# Test case 2 UI: Test the presence of buttons and textboxes
def test_buttons_and_textboxes(driver):
    """Test the presence of buttons and textboxes."""
    try:
        generate_button = driver.find_element(By.ID, 'generate')
        clear_button = driver.find_element(By.ID, 'clear')
        count_box = driver.find_element(By.ID, 'count')
        uuid_element = driver.find_element(By.ID, 'uuids')
        assert generate_button.is_displayed(), log_test_result("test_buttons_and_textboxes", "fail", "Generate button is not displayed!")
        assert clear_button.is_displayed(), log_test_result("test_buttons_and_textboxes", "fail", "Clear button is not displayed!")
        assert count_box.is_displayed(), log_test_result("test_buttons_and_textboxes", "fail", "Count box is not displayed!")
        assert uuid_element.is_displayed(), log_test_result("test_buttons_and_textboxes", "fail", "UUID element is not displayed!")
        log_test_result("test_buttons_and_textboxes", "pass")
    except AssertionError as e:
        log_test_result("test_buttons_and_textboxes", "fail", str(e))
        raise


def test_generate_uuid(driver):
    """Test the Generate button generates a UUID."""
    for _ in range(10):
        generate_button = driver.find_element(By.ID, 'generate')
        generate_button.click()
        uuid_element = driver.find_element(By.ID, 'uuids')
        uuid_text = uuid_element.text

        if uuid_text == "":
            print("Error: UUID was not generated!")
            assert False, "UUID was not generated!"
        else:
            print(f"Generated UUID: {uuid_text}")
            # Copy the UUID to the clipboard (if needed)
            driver.execute_script("navigator.clipboard.writeText(arguments[0]);", uuid_text)
            # Store the generated UUID in a text file
            with open("generated_uuid.txt", "a") as file:
                file.write(uuid_text + "\n")

def test_clear_uuid(driver):
    """Test the Clear button removes the UUID."""
    clear_button = driver.find_element(By.ID, 'clear')
    clear_button.click()
    uuid_element = driver.find_element(By.ID, 'uuids')
    assert uuid_element.text == "", "UUID was not cleared!"

def generate_multiple_uuids_10(driver):
    """Test adding 100 to the count box and generating multiple UUIDs."""
    count_box = driver.find_element(By.ID, 'count')
    count_box.clear()
    count_box.send_keys("10")
    
    generate_button = driver.find_element(By.ID, 'generate')
    generate_button.click()
    
    uuid_element = driver.find_element(By.ID, 'uuids')
    uuid_text = uuid_element.text
    
    if uuid_text == "":
        print("Error: UUIDs were not generated!")
        assert False, "UUIDs were not generated!"
    else:
        uuids = uuid_text.split("\n")
        assert len(uuids) == 10, "The number of UUIDs generated is not 10!"
        with open("generated_multiple_uuids.txt", "w") as file:
            for uuid in uuids:
                file.write(uuid + "\n")

def test_generate_multiple_uuids_1000(driver):
    """Test adding 10 to the count box and generating multiple UUIDs."""
    count_box = driver.find_element(By.ID, 'count')
    count_box.clear()
    count_box.send_keys("1000")
    
    generate_button = driver.find_element(By.ID, 'generate')
    generate_button.click()
    
    uuid_element = driver.find_element(By.ID, 'uuids')
    uuid_text = uuid_element.text
    
    if uuid_text == "":
        print("Error: UUIDs were not generated!")
        assert False, "UUIDs were not generated!"
    else:
        uuids = uuid_text.split("\n")
        with open("generated_multiple_uuids.txt", "w") as file:
            for uuid in uuids:
                file.write(uuid + "\n")

def test_get_results(driver):
    """Test the contents of the generated_multiple_uuids.txt file."""
    with open("generated_multiple_uuids.txt", "r") as file:
        uuids = file.readlines()
        assert len(uuids) == 1000, "The number of UUIDs generated is not 1000!"
        for uuid in uuids:
            assert uuid.strip() != "", "Empty UUID found in the file!"



