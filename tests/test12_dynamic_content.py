import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_factory import get_driver, quit_driver

# test data
url = "https://the-internet.herokuapp.com/"
expected_title = 'Dynamic Content'
expected_static_text_1 = "Accusantium eius ut architecto neque vel voluptatem vel nam eos minus ullam dolores voluptates enim sed voluptatem rerum qui sapiente nesciunt aspernatur et accusamus laboriosam culpa tenetur hic aut placeat error autem qui sunt."
expected_static_text_2 = "Omnis fugiat porro vero quas tempora quis eveniet ab officia cupiditate culpa repellat debitis itaque possimus odit dolorum et iste quibusdam quis dicta autem sint vel quo vel consequuntur dolorem nihil neque sunt aperiam blanditiis."
expected_static_image_1 = "https://the-internet.herokuapp.com/img/avatars/Original-Facebook-Geek-Profile-Avatar-5.jpg"
expected_static_image_2 = "https://the-internet.herokuapp.com/img/avatars/Original-Facebook-Geek-Profile-Avatar-6.jpg"
images_numbers = [0, 1, 2, 3, 4, 5, 6, 7]
expected_dynamic_images = [f"https://the-internet.herokuapp.com/img/avatars/Original-Facebook-Geek-Profile-Avatar-{number}.jpg" for number in images_numbers]


class TestDynamicContent(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/ul/li[12]/a").click()
        
    def test_title_is_correct(self):
        self.assertEqual(expected_title, self.driver.find_element(By.CSS_SELECTOR, "h3").text)
        self.driver.refresh()  # refreshing the page to test the dynamic/static content
        self.assertEqual(expected_title, self.driver.find_element(By.CSS_SELECTOR, "h3").text)

    def test_static_text(self):
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/p[2]/a").click()
        self.assertEqual(expected_static_text_1, self.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]').text)
        self.assertEqual(expected_static_text_2, self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]').text)
        self.driver.refresh()
        self.assertEqual(expected_static_text_1, self.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]').text)
        self.assertEqual(expected_static_text_2, self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]').text)

    def test_static_images(self):
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/p[2]/a").click()
        image_1 = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/img')
        image_2 = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/img')
        image_1_src = image_1.get_attribute('src')
        image_2_src = image_2.get_attribute('src')
        self.assertEqual(expected_static_image_1, image_1_src)
        self.assertEqual(expected_static_image_2, image_2_src)
        self.driver.refresh()
        self.assertEqual(expected_static_image_1, image_1_src)
        self.assertEqual(expected_static_image_2, image_2_src)
 
    def test_dynamic_text(self):
        self.assertIsInstance(self.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]').text, str)
        self.assertIsInstance(self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]').text, str)
        self.assertIsInstance(self.driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[2]').text, str)

    def test_dynamic_images(self):
        images = self.driver.find_elements(By.TAG_NAME, "img")
        for image in images:
            with self.subTest(image=image):
                self.assertEqual(image.tag_name, "img")
    
    def tearDown(self):
        quit_driver(self.driver)
