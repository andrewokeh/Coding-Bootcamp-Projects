from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

GOOGLE_FORM = ("your google form")
LISTINGS = ("https://homefinder.com/rentals/CA/San-Francisco?maxPrice=3000&map=1"
            "&latitude=37.72316797782803&longitude=-122.43842368798826&zoom=12")

response = requests.get(LISTINGS)
listings_web_page = response.text

soup = BeautifulSoup(listings_web_page, "html.parser")
listings = soup.find_all(name="a", class_="listing-tile")
listing_links = []

for listing in listings:
    listing_links.append("https://homefinder.com" + listing.get("href"))

prices = soup.find_all(name="div", class_="h4")
prices_list = []

for price in prices:
    prices_list.append(price.text.split()[0])

addresses = soup.find_all(name="div", class_="addr-component")
addresses_list = []
odd = True
hold = None

for address in addresses:
    if odd:
        hold = address.text.strip()  # Hold is hold the first line of each address and combine with second line
    else:
        addresses_list.append(hold + " " + address.text.strip())
    odd = not odd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM)

time.sleep(2)

for i in range(len(listing_links)):
    address_form = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]'
                                                       '/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_form.send_keys(addresses_list[i])
    price_form = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]'
                                                     '/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_form.send_keys(prices_list[i])
    link_form = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]'
                                                    '/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_form.send_keys(listing_links[i])
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]'
                                                        '/div[1]/div[1]/div/span/span')
    submit_button.click()
    time.sleep(1)

    submit_another = driver.find_element(By.LINK_TEXT, value="Submit another response")
    submit_another.click()
    time.sleep(1)
