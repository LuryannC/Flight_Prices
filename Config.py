import os
from random import randint, random
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
import undetected_chromedriver as uc


class ConfigClass:
    def __init__(self):
        # Configs
        self.start_from = "London"  # Departing airport
        self.destination = "GRU"  # Arriving airport
        self.chosen_day = ("10", "2022-12")  # Departing date
        self.chosen_return = ("01", "2023-02")  # Return date
        self.add_nearby = True  # Add nearby airports for destination

        self.random_version = f'{randint(80, 103)}.0.{randint(2000, 5013)}.{randint(10, 53)}'

        self.url = ["https://www.skyscanner.net", "https://www.skyscanner.net/sttc/px/captcha-v2/index.html",
                    "https://www.google.co.uk"]
        self.create_file = True

        # Driver options and user agent
        # Browser configs to bypass bot detection
        self.chrome_options = Options()
        self.ua = UserAgent()
        self.userAgent = self.ua.random
        # self.chrome_options.page_load_strategy = "normal"
        # self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.chrome_options.add_experimental_option('useAutomationExtension', False)
        # self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--incognito")
        # self.chrome_options.add_argument("--enable-javascript")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument(f'user-agent={self.userAgent}')
        # self.chrome_options.add_experimental_option("detach", True)
        os.environ['GH_TOKEN'] = "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"
        self.driver = uc.Chrome(options=self.chrome_options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)
        # self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """
        #         Object.defineProperty(navigator, 'webdriver', {
        #         get: () => undefined})
        #         """
        # })
        # self.driver.header_overrides = {
        #     'User-Agent': f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.random_version} Safari/537.36'}
        # self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        #     "userAgent": f'Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.random_version} Safari/537.36'})
        shadow = Shadow(self.driver)
