from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import NoSuchElementException
import os
from selenium.common.exceptions import WebDriverException

def dis(slink):
    districtLink = getDistrict(slink)
    for dlink in districtLink:
            try:# this try block use to handle the Exception
                disFun(slink.text, dlink.text) # this line call to create a folders
                blo(slink,dlink)
            except FileExistsError: # this Exception is used to handle the FileExistsError
                blo(slink,dlink)
               
def blo(slink,dlink):
    blockLink = getBlock(dlink)
    for blink in blockLink:
        try:# this try block use to handle the Exception
            blockFun(slink.text, dlink.text, blink.text) # this line call to create a folders
            fun(slink, dlink, blink)
        except FileExistsError: # this Exception is used to handle the FileExistsError
            continue

# create web driver
def driverFun(link):
    driver = webdriver.Chrome(executable_path='E:\chromedriver.exe') # this line is help to get a connection from Chrome using webdriver
    driver.get(link)
    return driver

# this functions using to create a folders
# using os command-(mkdir)
def stateFun(slink):
    os.mkdir('E:\\download\\'+slink)

def disFun(slink, dlink):
    os.mkdir('E:\\download\\'+slink+'\\'+dlink)

def blockFun(slink, dlink, blink):
    os.mkdir('E:\\download\\'+slink+'\\'+dlink+'\\'+blink)


# this functions using to get a webpage elements
# it will return the elements in list formate
def getState(link):
    driver = driverFun(link)
    # this line helps for-loop to get a elements and stored one in a list
    states = [slink for slink in driver.find_elements(By.XPATH, '//*[@id="form1"]/div[3]/center/table/tbody/tr/td/a')] 
    return states

def getDistrict(link):
    driver = driverFun(link.get_attribute('href'))
    districtLink = [dlink for dlink in driver.find_elements(By.XPATH, '//*[@id="gvdist"]/tbody/tr/td/a')]
    return districtLink

def getBlock(dlink):
    driver = driverFun(dlink.get_attribute('href'))
    blockLinks = [blink for blink in driver.find_elements(By.XPATH, '//*[@id="gvdpc"]/tbody/tr/td/a')]
    return blockLinks

# this function using to download a files one by one
# It will stored pecific locations
def fun(slink, dlink, blink):
    print(blink.text)

    # Next four line is to make a driver connection and set a pesific location
    op = webdriver.ChromeOptions()
    p = {'download.default_directory': 'E:\\download\\' +slink.text+'\\'+dlink.text+'\\'+blink.text}
    op.add_experimental_option('prefs', p)
    driver = webdriver.Chrome(executable_path='E:\chromedriver.exe', options=op)

    link = blink.get_attribute('href')
    driver.get(link)
    try: # this try block use to handle the Exception
        expenditure = driver.find_element(By.LINK_TEXT, 'Amount Sanctioned/Expenditure On Works')
        driver.get(expenditure.get_attribute('href'))

        # the next line is help to get a dropdown elements in a website
        dropdown = driver.find_element(By.XPATH, '/html/body/form/div[3]/center/table/tbody/tr[1]/td[4]/b/font/select')
        # the next lines is help to get a values in a dropdown
        panchayat = Select(dropdown)
        list = panchayat.options

        for i in range(2, len(list)):
            driver.get(link)
            try: # this try block use to handle the Exception
                expenditure = driver.find_element(By.LINK_TEXT, 'Amount Sanctioned/Expenditure On Works')
                driver.get(expenditure.get_attribute('href'))
                dropdown = driver.find_element(By.XPATH, '/html/body/form/div[3]/center/table/tbody/tr[1]/td[4]/b/font/select')
                panchayats = Select(dropdown)
                panchayats.select_by_index(i)
                driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Btnreport"]').click()
                driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_LinkButton1"]').click()

            except WebDriverException: # this Exception is used to handle the WebDriverException
                print("no : "+str(i)+" ==> no data found")
    except NoSuchElementException:# this Exception is used to handle the NoSuchElementException
        print("the service is unavailable")

# this codes is a main function
link = "https://nrega.nic.in/Netnrega/sthome.aspx"
# list variable 
stateLinks = getState(link)
for slink in stateLinks:
    try:
        stateFun(slink.text)
        dis(slink)
    except FileExistsError:
        dis(slink)