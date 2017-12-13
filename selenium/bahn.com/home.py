import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

dp = '../chromedriver_linux64/chromedriver'  # Driver path
service = webdriver.chrome.service.Service(dp)
service.start()

chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Remote(
	service.service_url,
	desired_capabilities=chrome_options.to_capabilities())
driver.get('https://www.bahn.com/en/view/index.shtml')

## Sequential processes
# Input depart information
inputBox1 = driver.find_element_by_id('js-auskunft-autocomplete-from')
inputBox1.send_keys('Aachen Hbf')
inputBox2 = driver.find_element_by_id('js-auskunft-autocomplete-to')
inputBox2.send_keys('Aalen')

departDate = driver.find_element_by_css_selector('.date-wrapper input.hasDatepicker')
ActionChains(driver).move_to_element(departDate).click().send_keys(13 * Keys.BACKSPACE).send_keys(13 * Keys.DELETE).send_keys('Sat, 23.12.17').perform()

departTime = driver.find_element_by_css_selector(
	"div#js-auskunft-timeinput input[name=time]")
ActionChains(driver).move_to_element(departTime).click().send_keys(5 * Keys.BACKSPACE).send_keys(5 * Keys.DELETE).send_keys('06:00').perform()

submitBtn = driver.find_element_by_css_selector(
	"fieldset.js-submit .js-submit-btn")
time.sleep(0.5)
submitBtn.click()
# Looking for result
resultRow = driver.find_elements_by_css_selector(
	"table#resultsOverview tbody.scheduledCon")
# Checking for date range
# lastDepart = 
laterBtn = driver.find_element_by_css_selector(
	"table#resultsOverview tr.links a.buttonGreyBg later")

# driver.page_source

time.sleep(5)
driver.quit()