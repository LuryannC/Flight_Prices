import os
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


class ConfigClass:
    def __init__(self):

        # Configs
        self.start_from = "London"
        self.destination = "NVT"
        self.chosen_day = ("10", "2022-12")
        self.chosen_return = ("30", "2023-01")

        self.url = ["https://www.skyscanner.net", "https://www.skyscanner.net/sttc/px/captcha-v2/index.html"]
        self.create_file = False
