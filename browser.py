import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def driver_options(options_list):
    options = Options()
    for option in options_list:
        options.add_argument(option)
    return options


def assembly_element(tag, property_elem, meaning):
    return f'//{tag}[@{property_elem}="{meaning}"]'


def get_profile():
    location = json.dumps({"location": {"lat": os.getenv("LAT"), "lng": os.getenv("LNG")}, "accuracy": 10.0})
    profile = FirefoxProfile()
    profile.set_preference('geo.prompt.testing', True)
    profile.set_preference('geo.prompt.testing.allow', True)
    profile.set_preference("geo.provider.testing", True)
    profile.set_preference('geo.provider.network.url',
                           f'data:application/json,{location}')
    return profile


class Browser:
    def __init__(self):
        options = ['--headless', '--no-sandbox', '--start-maximized', '--window-size=1024,600']
        options = driver_options(options)
        profile = get_profile()
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                        options=options,
                                        firefox_profile=profile)

    def go_to_page(self, url):
        try:
            self.driver.get(url=url)
            return True
        except:
            return None

    def close(self):
        try:
            self.driver.close()
            self.driver.quit()
            return True
        except:
            return None

    def wait_load_elem(self, element, timeout=10):
        for _ in range(timeout):
            try:
                var = self.driver.find_element_by_xpath(element)
                if var.location_once_scrolled_into_view:
                    return var
            except:
                sleep(1)

    def find_elem(self, element):
        if self.wait_load_elem(element, 20):
            try:
                var = self.driver.find_element_by_xpath(element)
                return var
            except:
                return None

    def click(self, element):
        clickable_elem = self.find_elem(element=element)
        if clickable_elem:
            try:
                clickable_elem.click()
                sleep(1)
                return True
            except:
                return None

    def click_by_text(self, text):
        element = f"//*[contains(text(), '{text}')]"
        if self.wait_load_elem(element) and self.find_elem(element) and self.click(element):
            sleep(1)
            return True

    def write_input(self, element, text):
        self.driver.find_element_by_xpath(element).send_keys(text)
        return True
