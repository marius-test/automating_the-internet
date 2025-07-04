import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.driver_factory import get_driver, quit_driver

# test data
url = "https://the-internet.herokuapp.com/"
expected_title = "Context Menu"
expected_text_1 = "Context menu items are custom additions that appear in the right-click menu."
expected_text_2 = "Right-click in the box below to see one called 'the-internet'. When you click it, it will trigger a JavaScript alert."
expected_alert_text = "You selected a context menu"


class TestContextMenu(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Context Menu']").click()

    def test_title_text(self):
        paragraph = self.driver.find_elements(By.TAG_NAME, "p")
        self.assertEqual(expected_title, self.driver.find_element(By.TAG_NAME, "h3").text)
        self.assertEqual(expected_text_1, paragraph[0].text)
        self.assertEqual(expected_text_2, paragraph[1].text)
        
    def test_box_properties(self):
        style = self.driver.find_element(By.ID, "hot-spot").get_attribute("style")
        self.assertEqual("border-style: dashed; border-width: 5px; width: 250px; height: 150px;", style)

    def test_alert_box_open(self):
        alert = Alert(self.driver)
        action = ActionChains(self.driver)
        box = self.driver.find_element(By.ID, "hot-spot")
        action.context_click(box).perform()
        self.assertEqual(expected_alert_text, alert.text)

    def test_alert_box_closed(self):
        alert = Alert(self.driver)
        action = ActionChains(self.driver)
        box = self.driver.find_element(By.ID, "hot-spot")
        action.context_click(box).perform()
        self.assertEqual(expected_alert_text, alert.text)
        alert.accept()
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
        except TimeoutException:
            alert_is_present = 'No'
        else:
            alert_is_present = 'Yes'
        finally:
            self.assertTrue(alert_is_present == 'No')

    def tearDown(self):
        quit_driver(self.driver)
