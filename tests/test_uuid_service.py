import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import re

#Test url
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
    
# Test case 1 UI: Test the page title and the presence of the <h1> element.    
def test_page_title(driver):
    """Test the presence of the <h1> element and its text."""
    try:
        driver.refresh()
        h1_element = driver.find_element(By.TAG_NAME, 'h1')
        assert h1_element.is_displayed(), log_test_result("Test 1: test_page_title", "fail", f"<h1> element is not displayed!")
        assert h1_element.text == "UUID Generator", log_test_result("Test 1: test_page_title", "fail", f"<h1> text is incorrect! Found: {h1_element.text}")
        log_test_result("Test 1: test_page_title", "pass")
    except AssertionError as e:
        log_test_result("Test 1: test_page_title", "fail", str(e))
        raise

# Test case 2 UI: Refresh the page and test the presence of buttons and textboxes
def test_buttons_and_textboxes(driver):
    """Test the presence of buttons and textboxes."""
    try:
        driver.refresh()
        generate_button = driver.find_element(By.ID, 'generate')
        clear_button = driver.find_element(By.ID, 'clear')
        count_box = driver.find_element(By.ID, 'count')
        uuid_element = driver.find_element(By.ID, 'uuids')
        assert generate_button.is_displayed(), log_test_result("Test 2: test_buttons_and_textboxes", "fail", "Generate button is not displayed!")
        assert clear_button.is_displayed(), log_test_result("Test 2: test_buttons_and_textboxes", "fail", "Clear button is not displayed!")
        assert count_box.is_displayed(), log_test_result("Test 2: test_buttons_and_textboxes", "fail", "Count box is not displayed!")
        assert uuid_element.is_displayed(), log_test_result("Test 2: test_buttons_and_textboxes", "fail", "UUID element is not displayed!")
        log_test_result("Test 2: test_buttons_and_textboxes", "pass")
    except AssertionError as e:
        log_test_result("Test 2: test_buttons_and_textboxes", "fail", str(e))
        raise

# Test case 3 UI: Test uuid generation and format. Generate 1 UUID, validate format and store it in a text file, raise error in case of failure.
def test_generate_single_uuid(driver):
    """Test the Generate button generates a UUID and generated uuid. store data in txt file in case of success."""
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    try:
            driver.refresh()
            generate_button = driver.find_element(By.ID, 'generate')
            generate_button.click()
            uuid_element = driver.find_element(By.ID, 'uuids')
            uuid_text = uuid_element.text
            if uuid_text == "":
                 assert False, log_test_result("Test 3:test_generate_single_uuid", "fail", f"uuid is not displayed!")
            else:
                assert uuid_pattern.match(uuid_text), log_test_result("Test 3: test_generate_single_uuid", "fail", f"Invalid UUID format: {uuid_text}")
                log_test_result("Test 3: test_generate_single_uuid", "pass")
                # Copy the UUID to the clipboard. This is a workaround for the issue with the clipboard not working in headless mode
                driver.execute_script("navigator.clipboard.writeText(arguments[0]);", uuid_text)
                # Store the generated UUID in a text file
                with open("generated_single_uuid.txt", "a") as file:
                    file.write(uuid_text + "\n")
    except AssertionError as e:
        log_test_result("Test 3: test_generate_single_uuid", "fail", str(e))
        raise  # Re-raise the exception to ensure the test fails  


# Test case 4 UI: Test genereate 10 UUIDs and store them in a text file. Raise error in case of failure. 
def test_generate_10_uuid(driver):
    """Test the Generate button generates a UUID and generated uuid. store data in txt file in case of success."""
    try:
        driver.refresh()
        for _ in range(10):
            generate_button = driver.find_element(By.ID, 'generate')
            generate_button.click()
            uuid_element = driver.find_element(By.ID, 'uuids')
            uuid_text = uuid_element.text

            if uuid_text == "":
                 assert False, log_test_result("Test 4: test_generate_10_uuid", "fail", f"uuid is not displayed!")
            else:
                # Copy the UUID to the clipboard. This is a workaround for the issue with the clipboard not working in headless mode
                driver.execute_script("navigator.clipboard.writeText(arguments[0]);", uuid_text)
                # Store the generated UUID in a text file
                log_test_result("Test 4: test_generate_10_uuid", "pass")
                with open("generated_uuid.txt", "a") as file:
                    file.write(uuid_text + "\n")
    except AssertionError as e:
        log_test_result("Test 4: test_generate_10_uuid", "fail", str(e))
        raise    

# Test case 5 UI: Test the clear button. Generate a UUID and then clear it. Raise error in case of failure.
def test_clear_uuid(driver):
    """Test the Clear button removes the UUID."""
    driver.refresh()
    try:
        generate_button = driver.find_element(By.ID, 'generate')
        generate_button.click()
        uuid_element = driver.find_element(By.ID, 'uuids')
        uuid_text = uuid_element.text
        if uuid_text == "":
            assert False, log_test_result("Test 5: test_clear_uuid", "fail", "UUID is not displayed!")
        clear_button = driver.find_element(By.ID, 'clear')
        clear_button.click()
        uuid_element = driver.find_element(By.ID, 'uuids')
        assert uuid_element.text == "",  log_test_result("Test 5: test_clear_uuid", "fail", "UUid is not cleared!")
        log_test_result("Test 5: test_clear_uuid", "pass")
    except AssertionError as e:
        log_test_result("Test 5: test_clear_uuid", "fail", str(e))
        raise  # Re-raise the exception to ensure the test fails  

# TEST CASE 6: Test generate 100 UUIDs
def test_generate_multiple_uuids_100(driver):
    """Test adding 100 to the count box and generating multiple UUIDs."""
    try:
        count_box = driver.find_element(By.ID, 'count')
        count_box.clear()
        count_box.send_keys("100")
    
        generate_button = driver.find_element(By.ID, 'generate')
        generate_button.click()
    
        uuid_element = driver.find_element(By.ID, 'uuids')
        uuid_text = uuid_element.text
    
        if uuid_text == "":
            assert False, log_test_result("Test 6: test_generate_multiple_uuids_100", "fail", "UUIDs are not displayed!")
        else:
            uuids = uuid_text.split("\n")
            assert len(uuids) == 100, log_test_result("Test 6: test_generate_multiple_uuids_100", "fail", f"Expected 100 UUIDs, but found {len(uuids)}")
            log_test_result("Test 6: test_generate_multiple_uuids_100", "pass")
            with open("generated_100_uuids.txt", "w") as file:
                for uuid in uuids:
                    file.write(uuid + "\n")
    except AssertionError as e:
        log_test_result("Test 6: test_generate_multiple_uuids_100", "fail", str(e))
        raise
             

# TEST CASE 7: Test the count box and generate 1000 UUIDs
def test_generate_multiple_uuids_1000(driver):
    """Test adding 1000 to the count box and generating multiple UUIDs."""
    try:
        count_box = driver.find_element(By.ID, 'count')
        count_box.clear()
        count_box.send_keys("1000")
    
        generate_button = driver.find_element(By.ID, 'generate')
        generate_button.click()
    
        uuid_element = driver.find_element(By.ID, 'uuids')
        uuid_text = uuid_element.text
    
        if uuid_text == "":
            assert False, log_test_result("Test 7: test_generate_multiple_uuids_1000", "fail", str(e))
        else:
            log_test_result("Test 7: test_generate_multiple_uuids_1000", "pass")  
            uuids = uuid_text.split("\n")
            with open("generated_1000_uuids.txt", "w") as file:
                for uuid in uuids:
                    file.write(uuid + "\n")
    except AssertionError as e:
        log_test_result("Test 7: test_generate_multiple_uuids_1000", "fail", str(e))
        raise

# TEST CASE 8: Test the 'Privacy Policy' link and validate the redirected page content.
def test_privacy_policy_link(driver):
    """Test the 'Privacy Policy' link and validate the redirected page content."""
    try:
        driver.refresh()
        privacy_link = driver.find_element(By.XPATH, '//a[contains(text(), "Privacy policy")]')
        assert privacy_link.is_displayed(), log_test_result("Test 8: test_privacy_policy_link", "fail", "'Privacy policy' link is not displayed!")
        privacy_link.click()
        driver.implicitly_wait(10)  # Wait for the page to load
        h1_element = driver.find_element(By.TAG_NAME, 'h1')
        assert h1_element.text.lower() == "privacy policy", log_test_result("Test 8: test_privacy_policy_link", "fail", "Redirected page title is incorrect!")
        assert "please respect the privacy of others." in driver.page_source.lower(), log_test_result("Test 8: test_privacy_policy_link", "fail", "Redirected page content is incorrect!")
        log_test_result("Test 8: test_privacy_policy_link", "pass")
    except AssertionError as e:
        log_test_result("Test 8: test_privacy_policy_link", "fail", str(e))
        raise
    except Exception as e:
        log_test_result("Test 8: test_privacy_policy_link", "fail", str(e))
        raise

# TEST CASE 9: Test the 'About Us' link and validate the redirected page content.
def test_about_us_link(driver):
    """Test the 'About Us' link and validate the redirected page content."""
    try:
        driver.refresh()
        about_link = driver.find_element(By.XPATH, '//a[contains(text(), "About Us")]')
        assert about_link.is_displayed(), log_test_result("Test 9: test_about_us_link", "fail", "'About Us' link is not displayed!")
        about_link.click()
        driver.implicitly_wait(10)  # Wait for the page to load
        h1_element = driver.find_element(By.TAG_NAME, 'h1')
        assert h1_element.text.lower() == "about us", log_test_result("Test 9: test_about_us_link", "fail", "Redirected page title is incorrect!")
        assert "we are a team of developers" in driver.page_source.lower(), log_test_result("Test 9: test_about_us_link", "fail", "Redirected page content is incorrect!")
        log_test_result("Test 9: test_about_us_link", "pass")
    except AssertionError as e:
        log_test_result("Test 9: test_about_us_link", "fail", str(e))
        raise
    except Exception as e:
        log_test_result("Test 9: test_about_us_link", "fail", str(e))
        raise

# TEST CASE 10: Test the 'Terms & conditions' link and validate the redirected page content.
def test_terms_and_conditions_link(driver):
    """Test the 'Terms & conditions' link and validate the redirected page content."""
    try:
        driver.refresh()
        terms_link = driver.find_element(By.XPATH, '//a[contains(text(), "Terms & conditions")]')
        assert terms_link.is_displayed(), log_test_result("Test 10: test_terms_and_conditions_link", "fail", "'Terms & conditions' link is not displayed!")
        terms_link.click()
        driver.implicitly_wait(10)  # Wait for the page to load
        h1_element = driver.find_element(By.TAG_NAME, 'h1')
        assert h1_element.text.lower() == "terms and conditions", log_test_result("Test 10: test_terms_and_conditions_link", "fail", "Redirected page title is incorrect!")
        assert "you must use this responsibly. thanks!." in driver.page_source.lower(), log_test_result("Test 10: test_terms_and_conditions_link", "fail", "Redirected page content is incorrect!")
        log_test_result("Test 10: test_terms_and_conditions_link", "pass")
    except AssertionError as e:
        log_test_result("Test 10: test_terms_and_conditions_link", "fail", str(e))
        raise
    except Exception as e:
        log_test_result("Test 10: test_terms_and_conditions_link", "fail", str(e))
        raise