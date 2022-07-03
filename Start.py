import os
from time import sleep
from Config import ConfigClass
from random import randint
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import jpype

jpype.startJVM()
from ExportData import *


class FlightBot:

    def __init__(self):
        self.config = ConfigClass()
        self.driver = self.config.driver
        self.main()
        self.data = None

    def main(self):
        self.driver.get(self.config.url[0])
        sleep(12)
        self.accept_cookies()
        sleep(randint(3, 6))
        self.start_search(self.config.start_from)
        sleep(randint(5, 8))
        self.get_data()
        sleep(3)
        try:
            os.makedirs('.\data', exist_ok=True)
        except OSError as error:
            return
        create_file('data', '{}-{} to {}-{}'.format(self.config.chosen_day[0], self.config.chosen_day[1], self.config.chosen_return[0], self.config.chosen_return[1]), self.data)

    def check_if_exists(self, by, path):
        try:
            self.driver.find_elements(by, path)
        except NoSuchElementException:
            return False  # , print("False, {} does not exist".format(path))
        return True  # , print("True, {} does exist".format(path))

    def accept_cookies(self):
        if self.check_if_exists(By.ID, 'acceptCookieButton'):
            self.driver.find_element(By.ID, 'acceptCookieButton').click()
        else:
            pass

    def start_search(self, origin):
        sleep(2)
        from_box_element = self.driver.find_element(By.XPATH, '//Input[@name="fsc-origin-search"]')
        from_box_element.click()
        sleep(randint(1, 2))
        from_box_element.send_keys(origin)
        sleep(randint(1, 2))
        self.driver.find_element(By.XPATH, '//ul/li[@id="react-autowhatever-fsc-origin-search--item-0"]').click()
        self.destination_handle(self.config.destination)

    def destination_handle(self, dest):
        sleep(0.2)
        destination_box_element = self.driver.find_element(By.XPATH, '//Input[@name="fsc-destination-search"]')
        destination_box_element.click()
        sleep(1)
        destination_box_element.send_keys(dest)
        sleep(1)
        self.driver.find_element(By.XPATH, '//ul/li[@id="react-autowhatever-fsc-destination-search--item-0"]').click()
        if self.config.add_nearby:
            sleep(0.2)
            self.driver.find_element(By.XPATH, '//input[@name="destinationFlexible"]').click()
        self.fill_dates()

    def fill_dates(self):
        sleep(0.3)
        # Starts with Depart
        # Get the depart box element
        self.driver.find_element(By.XPATH, '//button[@id="depart-fsc-datepicker-button"]').click()
        sleep(0.6)
        # Select the dropdown menu
        self.driver.find_element(By.XPATH, '//select[@id="depart-calendar__bpk_calendar_nav_select"]').click()
        sleep(0.6)
        # Select the month specified
        self.driver.find_element(By.XPATH, f'//option[@value="{self.config.chosen_day[1]}"]').click()
        # Select chosen day
        self.driver.find_element(By.XPATH,
                                 "//button//span[contains(text(), {})]".format(self.config.chosen_day[0])).click()
        sleep(1)
        # Return
        # Select return box element
        self.driver.find_element(By.XPATH, '//button[@id="return-fsc-datepicker-button"]').click()
        sleep(0.6)
        # Select the dropdown menu
        self.driver.find_element(By.XPATH, '//select[@id="return-calendar__bpk_calendar_nav_select"]').click()
        sleep(1)
        # Select the return month specified
        self.driver.find_element(By.XPATH, f'//select//option[@value="{self.config.chosen_return[1]}"]').click()
        sleep(1)
        # Select return day
        self.driver.find_element(By.XPATH,
                                 "//button[@class='BpkCalendarDate_bpk-calendar-date__MTdlO']//span[contains(text(), "
                                 "{})]".format(self.config.chosen_return[0])).click()
        sleep(1)
        self.driver.find_element(By.XPATH, "//button[@class='BpkButtonBase_bpk-button__NTM4Y "
                                           "BpkButtonBase_bpk-button--large__ZWQyM App_submit-button__NGFhZ "
                                           "App_submit-button-oneline__MmU3N']").click()
        sleep(5)

    def get_data(self):
        sleep(randint(12, 16))
        self.driver.find_element(By.XPATH,
                                 '//button[@class="DangerouslyUnstyledButton_container__NGM5Y DangerouslyUnstyledButton_enabled__ZDg1M FqsTabs_fqsTabWithSparkle__ZjA2Z"]').click()
        sleep(randint(3, 6))
        root_div = self.driver.find_elements(By.XPATH, '//div[@class="EcoTicketWrapper_itineraryContainer__ZWE4O"]')
        temp_list = []
        for div in root_div:
            departing_time = div.find_element(By.XPATH,
                                              './/span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--subheading__ODU3O"]').text
            departing_airport = div.find_element(By.XPATH,
                                                 './/span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--body-default__NGZhN LegInfo_routePartialCityTooltip__NTE4Z"]').text
            return_duration = div.find_element(By.XPATH,
                                               './/div[@class="UpperTicketBody_legsContainer__ZjcyZ"]//div[@class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN"][2]//div[@class="LegInfo_legInfo__ZGMzY"]//span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--xs__MWQxY Duration_duration__NmUyM"]').text
            arriving_time = div.find_element(By.XPATH,
                                             './/div[@class="LegInfo_routePartialArrive__Y2U1N"]//span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--lg__ODFjM LegInfo_routePartialTime__OTFkN"]//div//span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--subheading__ODU3O"]').text
            # To-do
            arriving_airport = 0  # div.find_element(By.XPATH,
            #                './/div[@class="LegInfo_routePartialArrive__Y2U1N"]//span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--body-default__NGZhN"]//span').text

            return_time = div.find_element(By.XPATH,
                                           './/div[@class="UpperTicketBody_legsContainer__ZjcyZ"]//div[@class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN"][2]//div[@class="LegInfo_legInfo__ZGMzY"]//div[@class="LegInfo_routePartialDepart__NzEwY"]//span//div//span').text
            return_airport = div.find_element(By.XPATH,
                                              './/div[@class="UpperTicketBody_legsContainer__ZjcyZ"]//div[@class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN"][2]//div[@class="LegInfo_legInfo__ZGMzY"]//div[@class="LegInfo_routePartialDepart__NzEwY"]//span[2]//span').text
            outbound_duration = div.find_element(By.XPATH,
                                                 './/span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--xs__MWQxY Duration_duration__NmUyM"]').text
            return_arrive_time = div.find_element(By.XPATH,
                                                  './/div[@class="UpperTicketBody_legsContainer__ZjcyZ"]//div[@class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN"][2]//div[@class="LegInfo_legInfo__ZGMzY"]//div[@class="LegInfo_routePartialArrive__Y2U1N"]//span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--subheading__ODU3O"]').text
            # TO-DO
            return_arrive_airport = 0  # div.find_element(By.XPATH,
            #         './/div[@class="UpperTicketBody_legsContainer__ZjcyZ"]//div[@class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN"][2]//div[@class="LegInfo_legInfo__ZGMzY"]//div[@class="LegInfo_routePartialArrive__Y2U1N"]//span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--body-default__NGZhN"]//span').text

            price = div.find_element(By.XPATH,
                                     './/span[@class="BpkText_bpk-text__YWQwM BpkText_bpk-text--lg__ODFjM"]').text
            flight_link = div.find_element(By.XPATH,
                                           './/a[@class="FlightsTicket_link__ODZjM"]').get_attribute('href')

            div_wrapped = (
                departing_time, departing_airport, outbound_duration, arriving_time, arriving_airport, return_time,
                return_airport, return_duration, return_arrive_time, return_arrive_airport, price, flight_link)
            temp_list.append(div_wrapped)
        self.data = temp_list
        return self.data


if __name__ == '__main__':
    FlightBot()
# jpype.shutdownJVM()
