from logging import log
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import ddddocr
import time
from PIL import Image
#import tesserocr
from PIL import Image
import numpy as np
import json

URL = 'https://portal.sysu.edu.cn/#/login'

# get data from config.json
def read_json():
    with open("config.json",'r') as data:
      res = json.load(data)
    return res
    
# write data to config.json
def write_json(username, password, ratio, driver_path):
	yadayo={
		'USERNAME':username,
		'PASSWORD':password,
		'RATIO':ratio,
		'DRIVER_PATH':driver_path
	}
	with open("config.json","w") as f:
		json.dump(yadayo,f)
		print("data written successfully...")
    
data = read_json()
username = data["USERNAME"]
password = data["PASSWORD"]
ratio = data['RATIO']
driver_path = data['DRIVER_PATH']

if not username or not password:
	print('initialize......')
	username = input('please enter your username:')
	password = input('please enter your password:')
	ratio = float(input('please enter ratio:'))
	driver_path = input('please enter path of geckodriver.exe:')
	write_json(username, password, ratio, driver_path)


ocr = ddddocr.DdddOcr()

options = webdriver.FirefoxOptions()
options.add_argument("--headless") #no head
driver = webdriver.Firefox(executable_path=driver_path,options=options)

driver.get(URL)
driver.find_element_by_css_selector('button[type="button"]').click()

# input username and password
driver.find_element_by_css_selector('input[id="username"]').send_keys(username)
driver.find_element_by_css_selector('input[id="password"]').send_keys(password)

# get pic of logweb
driver.save_screenshot("screenshot.png")

# Get the exact location
code_element = driver.find_element_by_css_selector('img[id="captchaImg"]')
left = code_element.location['x']
upper = code_element.location['y']
right = code_element.size['width']+left
lower = code_element.size['height']+upper

# get captchaImg
image = Image.open('screenshot.png')
code_image = image.crop((left*ratio, upper*ratio, right*ratio, lower*ratio))
pixdata = code_image.load()

# use ddddocr to get string
code = ocr.classification(code_image)

# enter string and login
driver.find_element_by_css_selector('input[id="captcha"]').send_keys(code)
driver.find_element_by_css_selector('input[class="btn btn-submit btn-block"]').click()

# go to jiankangshenbao
driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
time.sleep(3)

driver.find_element_by_css_selector('li[class="command_button"]').click()
time.sleep(3)
driver.find_element_by_css_selector('li[class="command_button"]').click()

driver.quit()

print('Congratuations for lazydog')
