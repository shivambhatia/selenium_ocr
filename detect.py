"""
Designed By: Shivam Bhatia
Date: 10/07/2021
Used to extract data from the given url using cloud vision api
to bypass the captcha text using OCR
"""

import urllib.request
from selenium import webdriver
from time import sleep
import os
import re
import urllib.request
import os
"""Defining the configuration for Chrome Driver and Cloud Vision Project Starts Here"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='vision-project-250707-cf23184124b4.json'
from google.cloud import vision
import re
from selenium.webdriver.support.ui import Select
import io    
client = vision.ImageAnnotatorClient() 
chrome_path = r"C:\Users\Admin\Downloads\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("window-size=600,400")
options.headless = True
driver = webdriver.Chrome(chrome_path,options=options)



def extractCaptchaFromImage(image):
    """
    Function will return the captcha extracted from image using cloud vision api
    input: screenshot image of the page
    return : captcha of 6 digits
    """ 
    with io.open(image, 'rb') as image_file:        
        content = image_file.read()    
    image = vision.Image(content=content)    

    response = client.text_detection(image=image)    
    texts = response.text_annotations   
    desc=[i.description for i in texts]
    captcha=''
    for i in desc:
        p=re.findall(r'(\d{6})', i)
        if p:
            captcha=p[0]
    return captcha


def extractTableData(driver):
    """
    Extract Data from the driver finding table xpath
    input:driver
    return list of data
    
    """
    rws = driver.find_elements_by_xpath("//table/tbody/tr")
    # len method is used to get the size of that list
    r = len(rws)
    # to get column count of table
    cols = driver.find_elements_by_xpath("//table/thead/tr/th")
    # len method is used to get the size of that list
    c = len(cols)
    
    elemt = []
    #iterate over the rows
    for i in range(1,r):
    # row data set to 0 each time in list
        row = []
        #iterate over the columns
        for j in range(1,c):
            # getting text from the ith row and jth column
            d=driver.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text
            row.append(d)
        #finally store and print the list in console
        elemt.append(row)

    return elemt

def fillFormData(driver,name,schemaName):
    """
    Fill form data and automate submit
    input :driver,party name,DRT/DRAT name    
    return :list of data
    """
    """Schema name should be very specific"""
    select = Select(driver.find_element_by_id('schemaname'))
    # select by visible text
    select.select_by_visible_text(schemaName)
    driver.find_element_by_id('name').send_keys(name)
    driver.save_screenshot("screenshot.png")
    captcha=extractCaptchaFromImage('screenshot.png')
    driver.find_element_by_class_name('captchatext1').send_keys(captcha)
    driver.find_element_by_id("submit1").click()
    rws = driver.find_elements_by_xpath("//table/tbody/tr")
    if rws:
        table_data=extractTableData(driver)
    else:
        return 'Invalid Data'
    return table_data
    
    

def main(url,name,schemaname):

    driver.get(url)
    driver.execute_script("window.scrollTo(0,1280)")
    data=fillFormData(driver,name,schemaname)
    driver.quit()

    return data
    


    
    
   
    