from flask import Flask, jsonify, Blueprint, request
from flask_cors import CORS
from config import Config
from db import write_to_db
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import re

api_blueprint = Blueprint('api', __name__)

URL = Config.URL

def run_test_generate_single_uuid():
    chromedriver_path = r"C:\Users\darwin\Documents\project\automation_autofleet\tests\chromedriver.exe"
    
    # Check if the file exists
    if not os.path.isfile(chromedriver_path):
        raise RuntimeError(f"chromedriver.exe not found at {chromedriver_path}")

    service = Service(executable_path=chromedriver_path)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    try:
        driver.refresh()
        generate_button = driver.find_element(By.ID, 'generate')
        generate_button.click()
        uuid_element = driver.find_element(By.ID, 'uuids')
        uuid_text = uuid_element.text
        if uuid_text == "":
            raise AssertionError("UUID is not displayed!")
        else:
            assert uuid_pattern.match(uuid_text), f"Invalid UUID format: {uuid_text}"
            return uuid_text
    except Exception as e:
        raise RuntimeError(f"Test failed: {str(e)}")
    finally:
        driver.quit()

@api_blueprint.route('/add_to_db', methods=['POST'])
def add_to_db():
    try:
        uuid_text = run_test_generate_single_uuid()
        data = {"uuid": uuid_text}
        result = write_to_db("uuid", data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_app(testing=False):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app