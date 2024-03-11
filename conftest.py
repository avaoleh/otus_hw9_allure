import pytest
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeServise
from selenium.webdriver.firefox.service import Service as FirefoxService

from dotenv import load_dotenv
from opencart.utils import attach
import logging
import datetime

load_dotenv()
OPENCART_URL = os.getenv("OPENCART_LINK")


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--drivers", default=os.path.expanduser("~/Downloads/drivers"))
    parser.addoption("--log_level", action="store", default="INFO")

@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    drivers = request.config.getoption("--drivers")

    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info("===> Test %s started at %s" % (request.node.name, datetime.datetime.now()))

    if browser == "chrome":
        service = ChromeServise()
        driver = webdriver.Chrome(service=service)
    elif browser == "firefox":
        service = FirefoxService()
        driver = webdriver.Firefox(service=service)
    else:
        raise Exception("Driver not supported")

    driver.maximize_window()
    driver.get(OPENCART_URL)

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name

    logger.info("Browser %s started" % browser)

    def fin():
        driver.quit()
        logger.info("===> Test %s finished at %s" % (request.node.name, datetime.datetime.now()))

    request.addfinalizer(fin)
    return driver
