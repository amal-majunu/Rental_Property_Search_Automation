from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import config
from bs4 import BeautifulSoup

chrome_driver_path = config.driver_path
driver = webdriver.Chrome(executable_path=chrome_driver_path)

headers = config.headers
url = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.85814866321172%2C%22east%22%3A-122.29840365771484%2C%22south%22%3A37.69234228071924%2C%22west%22%3A-122.56825534228516%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
addr = []
table = soup.select("article div div a address")
for x in table:
    addr.append(x.getText())
    # print(x.getText())

price = soup.select('.iMKTKr')
rent = []

for x in price:
    # rent.append(x.getText())
    val = x.getText()
    rent.append(val)
    #print(x.getText())

links = soup.find_all('a','property-card-link',href=True)
ref_link = []
i = 0
for x in links:
    i += 1
    if i%2 != 0:
        continue
    y = x['href']
    print(y)
    if(y[0]=='/'):
        y = 'https://www.zillow.com'+y
    ref_link.append(y)
    # print(x['href'])
print(addr)
print(rent)
print(ref_link)

time.sleep(5)
for i in range(len(addr)):
    driver.get(config.form_link)
    inputs = driver.find_elements_by_class_name("zHQkBf")
    inputs[0].send_keys(addr[i])
    if len(rent) > 0:
        inputs[1].send_keys(rent[i])
    inputs[2].send_keys(ref_link[i])
    submit = driver.find_element_by_class_name("QvWxOd")
    submit.click()

