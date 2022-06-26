import os
import re
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from pyshadow.main import Shadow
# Dealing with excel files
import jpype
import asposecells

jpype.startJVM()
from asposecells.api import FileFormatType, Workbook

import Config

config = Config.ConfigClass()
#
# Configs
start_from = "London"
destination = "NVT"
chosen_day = ("10", "2022-12")
chosen_return = ("30", "2023-01")

url = ["https://www.skyscanner.net", "https://www.skyscanner.net/sttc/px/captcha-v2/index.html"]
create_file = False

# Create a new XLSX workbook
if config.create_file:
    wb = Workbook(FileFormatType.XLSX)
    # Insert value in the cells
    wb.getWorksheets().get(0).getCells().get("A1").putValue("Hello World")
    # Save workbook
    wb.save("./data/workbook.xlsx")
    jpype.shutdownJVM()

# Driver options and user agent
chrome_options = Options()
ua = UserAgent()
userAgent = ua.random
chrome_options.page_load_strategy = "normal"
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_experimental_option("detach", True)
os.environ['GH_TOKEN'] = "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"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.header_overrides = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.2785.143 Safari/537.36'})
shadow = Shadow(driver)


def check_if_exists(by, path):
    try:
        driver.find_elements(by, path)
    except NoSuchElementException:
        return False, print("False, {} does not exist".format(path))
    return True, print("True, {} does exist".format(path))


def bypass_captcha():
    empty_list = []
    # m = driver.find_element(By.XPATH, "//iframe[contains(@style,'display: block')]//").size.get()
    # print(m)
    ## iframe = driver.find_element(By.XPATH, "//iframe[contains(@style,'display: block')]")
    # iframe.find_element(By.XPATH, '//div[@aria-label="Click and hold"]')
    # print('Switched')
    # if check_if_exists(By.XPATH, '//section[@class="App_App__captcha__ZTE2M"]'):
    #     if check_if_exists(By.XPATH, '//div[@aria-label="Click and hold"]'):
    #         sleep(5)
    #         driver.find_element(By.XPATH, '//div//preceding::div[@aria-label="Click and hold"]').click()
    #         print('reached')


def accept_cookies():
    if check_if_exists(By.ID, 'acceptCookieButton'):
        driver.find_element(By.ID, 'acceptCookieButton').click()
    else:
        pass


def origin_handle(origin):
    sleep(2)
    from_box_element = driver.find_element(By.XPATH, '//Input[@name="fsc-origin-search"]')
    from_box_element.click()
    sleep(randint(1, 2))
    from_box_element.send_keys(origin)
    sleep(randint(1, 2))
    driver.find_element(By.XPATH, '//ul/li[@id="react-autowhatever-fsc-origin-search--item-0"]').click()
    destination_handle(destination)


def destination_handle(dest):
    sleep(0.2)
    destination_box_element = driver.find_element(By.XPATH, '//Input[@name="fsc-destination-search"]')
    destination_box_element.click()
    sleep(1)
    destination_box_element.send_keys(dest)
    sleep(1)
    driver.find_element(By.XPATH, '//ul/li[@id="react-autowhatever-fsc-destination-search--item-0"]').click()
    sleep(0.2)
    driver.find_element(By.XPATH, '//input[@name="destinationFlexible"]').click()
    fill_dates()


def fill_dates():
    sleep(0.3)
    # Starts with Depart
    # Get the depart box element
    driver.find_element(By.XPATH, '//button[@id="depart-fsc-datepicker-button"]').click()
    sleep(0.6)
    # Select the dropdown menu
    driver.find_element(By.XPATH, '//select[@id="depart-calendar__bpk_calendar_nav_select"]').click()
    sleep(0.6)
    # Select the month specified
    driver.find_element(By.XPATH, f'//option[@value="{chosen_day[1]}"]').click()
    # Select chosen day
    driver.find_element(By.XPATH, "//button//span[contains(text(), {})]".format(chosen_day[0])).click()
    sleep(1)
    # Return
    # Select return box element
    driver.find_element(By.XPATH, '//button[@id="return-fsc-datepicker-button"]').click()
    sleep(0.6)
    # Select the dropdown menu
    driver.find_element(By.XPATH, '//select[@id="return-calendar__bpk_calendar_nav_select"]').click()
    sleep(1)
    # Select the return month specified
    driver.find_element(By.XPATH, f'//select//option[@value="{chosen_return[1]}"]').click()
    sleep(1)
    # Select return day
    driver.find_element(By.XPATH, "//button[@class='BpkCalendarDate_bpk-calendar-date__MTdlO']//span[contains(text(), "
                                  "{})]".format(chosen_return[0])).click()
    sleep(1)
    driver.find_element(By.XPATH, "//button[@class='BpkButtonBase_bpk-button__NTM4Y "
                                  "BpkButtonBase_bpk-button--large__ZWQyM App_submit-button__NGFhZ "
                                  "App_submit-button-oneline__MmU3N']").click()
    sleep(5)


# Start bot
driver.get(url[1])
sleep(randint(3, 6))
bypass_captcha()
# accept_cookies()
# origin_handle(start_from)
# new_window = driver.window_handles[0]
# driver.switch_to.window(new_window)
# check_if_exists(By.XPATH, '//button[@class="DangerouslyUnstyledButton_container__NGM5Y DangerouslyUnstyledButton_enabled__ZDg1M FqsTabs_fqsTabWithSparkle__ZjA2Z FqsTabs_fqsTabWithSparkleSelected__MjNkM"]')
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()
