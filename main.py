# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from loguru import logger

from browser import Browser, assembly_element

load_dotenv()


def login():
    driver.go_to_page('https://tinder.com/app/login')
    driver.click_by_text(os.getenv('OTHER_OPTIONS').encode('cp1251').decode('utf8'))
    if driver.click_by_text(os.getenv('GO_TO_FACEBOOK').encode('cp1251').decode('utf8')) is None:
        driver.click('/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[2]/button')
    driver.driver.switch_to.window(driver.driver.window_handles[1])
    email = driver.write_input(assembly_element('input', 'id', 'email'), os.getenv('LOGIN'))
    password = driver.write_input(assembly_element('input', 'id', 'pass'), os.getenv('PASSWORD'))
    if email and password:
        driver.click(assembly_element('input', 'name', 'login'))
    else:
        return False
    driver.driver.switch_to.window(driver.driver.window_handles[0])
    a = os.getenv('ALLOW')
    driver.click_by_text(os.getenv('ALLOW').encode('cp1251').decode('utf8'))
    driver.click_by_text(os.getenv('TURN_ON').encode('cp1251').decode('utf8'))
    driver.go_to_page('https://tinder.com/app/recs')
    driver.click_by_text(os.getenv('AGREE').encode('cp1251').decode('utf8'))
    driver.click_by_text(os.getenv('NO_THANKS').encode('cp1251').decode('utf8'))
    return True


def get_element(xpath, len_=None):
    try:
        elements = driver.driver.find_elements_by_xpath(xpath)
        if len_:
            return len(elements)
        else:
            return elements[0]
    except:
        return None


def like():
    for _ in range(500):
        no_thanks = get_element(f"//*[contains(text(), '{os.getenv('NO_THANKS').encode('cp1251').decode('utf8')}')]")
        active = get_element(f"//*[contains(text(), '{os.getenv('RECENTLY_ACTIVE').encode('cp1251').decode('utf8')}')]", True)
        if no_thanks:
            finish = get_element(f"//*[contains(text(), '{os.getenv('OUT_OF_LIKES').encode('cp1251').decode('utf8')}')]")
            if finish:
                return True
            no_thanks.click()
        if active > 1:
            driver.click(
                '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[4]/button')  # like
        else:
            driver.click(
                '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button')  # dislike


if __name__ == '__main__':
    driver = Browser()
    if login() and like():
        logger.debug('finish by end like')
    else:
        logger.debug('finish by error')
    driver.close()
