import os
import re
import time
# from telnetlib import EC
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

# Configs
start_from = "London"
destination = "NVT"
chosen_day = ("10", "2022-12")
chosen_return = ("30", "2023-01")

url = "https://www.skyscanner.net"
searched = False


def check_if_exists(by, path):
    try:
        driver.find_element(by, path)
    except NoSuchElementException:
        return False, print("False, {} does not exist".format(path))
    return True, print("True, {} does exist".format(path))


def bypass_captcha():
    # sleep(2)
    captcha_path = driver.find_element(By.XPATH, '//p[contains(.,"Click and Hold")]')
    action = ActionChains(driver)
    click = ActionChains(driver)
    frame_x = captcha_path.location['x']
    frame_y = captcha_path.location['y']
    x_move = frame_x + captcha_path.size['width'] * 0.5
    y_move = frame_y + captcha_path.size['height'] * 0.5
    # action.move_to_element_with_offset(captcha_path, x_move, y_move).click_and_hold().perform()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@role="button"]//div//p[contains(., "Click and hold")]//preceding::div[1]'))).click()
    action.click_and_hold(captcha_path)
    action.perform()
    time.sleep(10)
    action.release(captcha_path)
    action.perform()
    time.sleep(0.2)
    action.release(captcha_path)


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



chrome_options = Options()
ua = UserAgent()
userAgent = ua.random
chrome_options.page_load_strategy = "normal"
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.add_argument("window-size=1280,800") chrome_options.add_argument( "user-agent=Mozilla/5.0 (Windows
# NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
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
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.2785.143 Safari/537.36'})

# Start bot
driver.get(url)
sleep(randint(3, 6))
# bypass_captcha()
accept_cookies()
origin_handle(start_from)
new_window = driver.window_handles[0]
driver.switch_to.window(new_window)
check_if_exists(By.XPATH, '//button[@class="DangerouslyUnstyledButton_container__NGM5Y DangerouslyUnstyledButton_enabled__ZDg1M FqsTabs_fqsTabWithSparkle__ZjA2Z FqsTabs_fqsTabWithSparkleSelected__MjNkM"]')
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()
