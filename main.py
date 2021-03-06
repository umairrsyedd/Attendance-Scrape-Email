import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime

print("Starting Automated Testing")
username = input("Enter The Username Of Knowledge Pro\n")
password = input("Enter The Password Of Knowledge Pro\n")
recipient = input("Enter Email To Send Alerts\n")
driver = webdriver.Chrome(ChromeDriverManager().install())
#Automated Selenium Testing
driver.get('http://www.google.com/')
search_box = driver.find_element_by_name('q')
search_box.send_keys('Presidency Knowledge Pro')
search_box.submit()
knowledgepro = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a/h3/span')
knowledgepro.click()
time.sleep(3)
usernameinput = driver.find_element_by_id('username')
passwordinput = driver.find_element_by_id('password')
usernameinput.send_keys(username)
passwordinput.send_keys(password)
login = driver.find_element_by_id("Login")
login.click()
print("Successfully Logged Into Knowledge Pro\n")
sidebar = driver.find_element_by_id("sidebar_main_toggle")
sidebar.click()
attendancePage = driver.find_element_by_xpath('//*[@id="sidebar_main"]/div/div[1]/div[2]/ul/li[1]/a')
attendancePage.click()
page_source = driver.page_source
driver.quit()
# BEAUTIFUL SOUP Extraction
soup = BeautifulSoup(page_source, features='lxml')
data = []
table = soup.find("table")
table_body = table.find("tbody")
rows = table_body.findAll("tr")
for row in rows:
    cols = row.findAll("td")
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
print("Uncleaned Data received")
print("Data : ")
print(data)
print("\n")
time.sleep(3)
dataClean1 = list(filter(None, data))  # Remove Empty List
dataClean2 = dataClean1[2:-3]  # Remove First Unnecessary and Last Unnecessary Row
lessAttendance = {}
borderAttendance = {}
goodAttendance = {}
print("\nData Cleaned Successfully\n")
time.sleep(2)
for subject in dataClean2:
    try:
        first = int(subject[0])
        temp = float(subject[-1])
        if temp < 75:
            print("Low Attendance In " + subject[1])
            lessAttendance[subject[1]] = temp
        elif 85 > temp > 75:
            print("BorderLine Attendance In " + subject[1])
            borderAttendance[subject[1]] = temp
        else:
            print("Good Attendance In " + subject[1])
            goodAttendance[subject[1]] = temp
    except ValueError:
        continue

leastString = ""
for subject, marks in lessAttendance.items():
    temp = str(subject) + " : " + str(marks)
    leastString = leastString + "\n" + temp
borderString = ""
for subject, marks in borderAttendance.items():
    temp = str(subject) + " : " + str(marks)
    borderString = borderString + "\n" + temp
goodString = ""
for subject, marks in goodAttendance.items():
    temp = str(subject) + " : " + str(marks)
    goodString = goodString + temp
print("\nLow Attendance And Border Attendance Subjects Obtained\n")
time.sleep(2)
email = "201810100741@presidencyuniversity.in"
password = "Uzair2005"
print("Initiating Email Process")
time.sleep(2)
# Initiating Email
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
print("Email Id Setup Complete")
msg = EmailMessage()
msg.set_content("The Following Courses Have VERY LOW ATTENDANCE : %s\n\nThese Courses Are In The Border Line : %s " % (
    leastString, borderString))
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
msg['Subject'] = 'Attendance Alerts Auto Generated [%s]' % current_time
msg['From'] = email
msg['To'] = recipient
smtpObj.login(email, password)
# Sending Email To User
smtpObj.send_message(msg)
print("\n\nEmail Sent To User : %s\n" % recipient)
smtpObj.quit()
# End Of Program
