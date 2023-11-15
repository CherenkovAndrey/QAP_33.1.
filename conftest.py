from selenium import webdriver
import pytest


@pytest.fixture(autouse=True)
def browser():
   driver = webdriver.Chrome('C:\\Users\\123\\Downloads\\chromedriver-win64\\chromedriver.exe')

   yield driver
   driver.quit()