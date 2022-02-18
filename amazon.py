import json
import time
import datetime
import pyautogui
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from gmail import Gmail


class AmazonOperation:
    def __init__(self):
        self.chrome_driver = ChromeDriverManager().install()

        self.ranking_ele_path = '//div[@class="zg-grid-general-faceout"]'
        self.ranking_title_ele_path = './div/a[2]/span/div'
        self.ranking_detail_ele_path = '//div[@id="detailBulletsWrapper_feature_div"]'

        with open('./json/setting.json') as setting:
            setting = json.load(setting)
            self.product_url = setting['product_url']
            self.ranking_page_urls = setting['ranking_page_urls']
            self.target_product_name = setting['target_product_name']
            self.to_address = setting['to_address']
            self.target_rank = setting['target_rank']


    def driver_start(self):
        self.driver = webdriver.Chrome(self.chrome_driver)


    def driver_close(self):
        self.driver.close()
        self.driver.quit()


    def take_ranking_screen_shot(self):
        self.driver.maximize_window()
        self.driver.get(self.product_url)
        element = self.driver.find_element(By.XPATH, self.ranking_detail_ele_path)
        self.scroll_by_el_and_offset(element, -10)
        time.sleep(2)
        file_name = self.take_screenshot()
        gmail = Gmail(file_name)
        gmail.send(self.to_address)


    def ranking_check(self) -> bool:
        is_ranking = False
        self.driver.maximize_window()

        for ranking_url in self.ranking_page_urls:
            self.driver.get(ranking_url)
            time.sleep(5)

            rankings = self.driver.find_elements(By.XPATH, self.ranking_ele_path)
            for rank in range(self.target_rank):
                title = rankings[rank].find_element(By.XPATH, self.ranking_title_ele_path).text
                if title == self.target_product_name:
                    is_ranking = True
                    break

            if is_ranking:
                break

        return is_ranking


    def scroll_by_el_and_offset(self, element: WebElement, offset: int = 0):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        if (offset != 0):
            script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
            self.driver.execute_script(script)


    def take_screenshot(self) -> str:
        dt_now = datetime.datetime.now()
        file_name = dt_now.strftime('%Y-%m-%d_%H-%M-%S') + '.png'
        screenshot = pyautogui.screenshot()
        screenshot.save(f"image/{file_name}")
        return file_name
