#!/usr/bin/env python3

import pickle
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import collections
collections.Callable = collections.abc.Callable
from bs4 import BeautifulSoup
import time

# author : christopher thiefin
# last update : 06-11-2023



your_user_email = "************************@gmail.com"
your_password = "************************"
the_activity = "https://www.linkedin.com/feed/update/urn:li:activity:7117879867798421504/"





def create_selenium():
	options = webdriver.ChromeOptions()
	options.add_argument('user-data-dir=/root/selenium')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(options=options)
	return driver







print("[+] Creating the webdriver instance")
driver = create_selenium()
print("[+] Checking login state")
driver.get("https://linkedin.com/uas/login")
time.sleep(1)
try:
	username = driver.find_element(By.ID, "username")
	username.send_keys(your_user_email)
	pword = driver.find_element(By.ID, "password")
	pword.send_keys(your_password)
	driver.find_element(By.XPATH, "//button[@type='submit']").click()
	print("[+] Connecting...")
	time.sleep(15)
except:
	pass

print("[+] Openning activity and getting reactions")
driver.get(the_activity)
time.sleep(1)
driver.implicitly_wait(10)
button = driver.find_element(By.CLASS_NAME, u"social-details-social-counts__social-proof-text")
ActionChains(driver).move_to_element(button).click(button).perform()
time.sleep(1)


print("[+] Retrieving more reactions")
div_element = driver.find_element(By.XPATH, "//div[@class='scaffold-finite-scroll__content']")
actions = ActionChains(driver)
allreactions = div_element.find_element(By.TAG_NAME, "ul")
li_elements = allreactions.find_elements(By.TAG_NAME, "li")
for li_element in li_elements:
	driver.execute_script("arguments[0].scrollIntoView(true);", li_element)
	actions.move_to_element(li_element).perform()
time.sleep(1)
try:
	for i in range(1,40):
		button = driver.find_element(By.CLASS_NAME, u"scaffold-finite-scroll__load-button")
		ActionChains(driver).move_to_element(button).click(button).perform()
		time.sleep(0.2)
except:
	pass


print("[+] Switching into like section and get all reactors")
like_div = driver.find_element(By.CLASS_NAME, u"social-details-reactors-tab__tablist")
like_button = like_div.find_elements(By.TAG_NAME, "button")
ActionChains(driver).move_to_element(like_button[1]).click(like_button[1]).perform()
time.sleep(5)


print("[+] Extracting source page and collecting profile url")
src = driver.page_source
soup = BeautifulSoup(src, 'lxml')
ul_list = soup.find("ul", {'class': 'artdeco-list--offset-1'})
person = ul_list.find_all("a", {'class': 'link-without-hover-state'})
print("[+] Profiles count : "+str(len(person)))
print("\n[+] Starting invitations !!\n")
for profile_url in person:
	try:
		start_name = str(profile_url).find("<span dir=\"ltr\">")
		end_name = str(profile_url).find("</span>")
		name = str(profile_url)[(start_name+16):(end_name-1)]
		if(len(name)>30):
			raise
		print("[+] Openning " +str(name)+ " profile")
		url_start = str(profile_url).find("https://www.linkedin.com/in")
		url_end = str(profile_url).find("\" id=\"ember")
		url = str(profile_url)[url_start:url_end]
		driver.get(url)
		time.sleep(1)
		try:
			driver.find_element(By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']").click()
			time.sleep(1)
		except:
			print("[!] Error on " +str(name)+ " profile")
		try:
			driver.find_element(By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']").click()
			time.sleep(1)
			print("[+] Invitation sent to " +str(name))
		except:
			print("[!] Already in relationship with " +str(name))
			pass
			# already friend
	except:
		pass
