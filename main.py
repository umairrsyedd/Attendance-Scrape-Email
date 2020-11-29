import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

print("Starting Automated Testing")
username = input("Enter The Username Of Knowledge Pro\n")
password = input("Enter The Password Of Knowledge Pro\n")

driver.get('http://www.google.com/');
search_box = driver.find_element_by_name('q')
search_box.send_keys('Presidency Knowledge Pro')
search_box.submit()
knowledgepro = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a/h3/span')
knowledgepro.click()
usernameinput = driver.find_element_by_id('username')
passwordinput = driver.find_element_by_id('password')
usernameinput.send_keys(username)
passwordinput.send_keys(password)
login = driver.find_element_by_id("Login")
login.click()
sidebar = driver.find_element_by_id("sidebar_main_toggle")
sidebar.click()
attendancePage = driver.find_element_by_xpath('//*[@id="sidebar_main"]/div/div[1]/div[2]/ul/li[1]/a')
attendancePage.click()
time.sleep(5)
driver.quit()
