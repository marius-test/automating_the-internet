import unittest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PATH = Service("C:\\Users\\marius\\webdriver\\chromedriver.exe")
chrome_service = Service(ChromeDriverManager().install())
url = "https://the-internet.herokuapp.com/"


class TestBrokenImages(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.get(url)
        self.driver.maximize_window()
    
    def test_broken_images(self):
        self.driver.find_element(By.CSS_SELECTOR, "a[href='/broken_images']").click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        image_list = self.driver.find_elements(By.TAG_NAME, "img")
        broken_images = 0
        for image in image_list:
            response = requests.get(image.get_attribute('src'), stream=True)
            if response.status_code != 200:
                broken_images += 1
        self.assertEqual("0", str(broken_images))
    
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
