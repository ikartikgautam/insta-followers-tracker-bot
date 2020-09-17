from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import configparser as cfg
# initialize the webdrivers
driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.instagram.com/')
# Get username and password from config.cfg
config = cfg.ConfigParser()
config.read('config.cfg')
uname = config.get('creds', 'username')
passWord = config.get('creds', 'password')
# Wait
driver.implicitly_wait(10)
# Sign In Using Username & Password
searchbox = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
searchbox.send_keys(uname)
searchbox = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
searchbox.send_keys(passWord)
searchBtn = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
searchBtn.click()
# Skip the pop-ups appeared on sign in
saveLogin = driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div/div/div/button')
saveLogin.click()
notifBtn = driver.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]')
notifBtn.click()
# Navigate to the profile
driver.get('https://www.instagram.com/'+uname+'/followers/')
# Get the number of followers
temp = 0
max = 0
profileHtml = driver.page_source
soup = BeautifulSoup(profileHtml, "html.parser")
for e in soup.find_all(class_="g47SY"):
    max = e.get_text()
    print('max = '+str(max))
    print("temp = "+str(temp))
    if(int(max) >= int(temp)):
        temp = max
# Open Followers Pop Up
followersBtn = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
followersBtn.click()
# Scroll The followers Pop up
fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
scroll = 0
while scroll < 100:
    driver.execute_script(
        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
    time.sleep(.5)
    scroll += 1

fList = driver.find_elements_by_xpath("//div[@class='isgrP']//li")
# print("fList len is {}".format(len(fList)))
# print("ended")

# Save the records in file
f = open("new.txt", 'w', encoding='utf-8')
i = 0
while i < len(fList):
    print('Writing => '+str(((i+1)/len(fList)*100)))
    f.write(fList[i].text.split('\n')[0]+'*#*')
    i = i+1
f.close()
# Read from file
f = open("new.txt", 'r', encoding='utf-8')
res = f.read()
newArr = res.split('*#*')
f.close()
#
old = open("old.txt", 'r', encoding='utf-8')
oldRes = old.read()
oldArr = oldRes.split('*#*')
old.close()
#
print("Got Followers : ")
for e in newArr:
    if (e in oldArr) == False:
        print(e)
print("Lost Followers : ")
for e in oldArr:
    if (e in newArr) == False:
        print(e)
#

if input("Do you want to replace old and new records ?[y/n]: "):
    f = open('old.txt', 'w', encoding='utf-8')
    for e in newArr:
        f.write(e+'*#*')
    print('DONE')        
