from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import requests
from pushover import Client
from datetime import datetime

client = Client('<ENTER YOUR CLIENT SECRET>', api_token='<API TOKEN>')

#Refresh Time set to 1 hr
refresh_time=3600

bestbuy_link='add link'
ebGames_link='add link'
target_link='add link'
newegg_link='add link'

class Stockr:
	def __init__(self):
		PROXY = "socks5://127.0.0.1:9050"
		chrome_options = Options()
		chrome_options.add_argument(" — incognito")
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument("--headless") 
		chrome_options.add_argument('--proxy-server=%s' % PROXY)
		self.driver = webdriver.Chrome(executable_path='chromedriver',options=chrome_options)
		self.timeout=30

	def BestBuy(self, link):
		self.driver.get(link)
		time.sleep(1)
		btn=WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="test"]/button')))
		avail=btn.is_enabled()
		if avail:
			status='In Stock'
		else:
			status = 'Out of Stock'
		time.sleep(2)
		return status

	def ebGames(self, link):
		self.driver.get(link)
		time.sleep(1)
		btn=WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME,'bigBuyButtons'))).text
		try:
			if 'ADD TO CART' in btn:
				status='In Stock'	
			elif 'OUT OF STOCK' in btn:
				status = 'Out of Stock'	
			else:
				status = 'Something is wrong with your code'
		except:
			print('ERROR...quiting')

		time.sleep(2)
		return status
		
	def target(self, link):
		self.driver.get(link)
		time.sleep(1)
		try:
			btn=WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="viewport"]/div[5]/div/div[2]/div[3]/div[1]/div/div[3]/div[1]/div[2]/button')))
			if btn.is_enabled():
				status='In Stock'
		except:
			status = 'Out of Stock'
		time.sleep(2)
		return status

	def newegg(self,link):
		self.driver.get(link)
		try:
			btn=WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ProductBuy"]/div/div[2]')))
			if btn.is_enabled():
				status='In Stock'
		except:
			status = 'Out of Stock'
		return status


def main():
	S=Stockr()

	while True:
		print('Current Run Time: ',datetime.now())

		if (S.BestBuy(bestbuy_link)=='In Stock'):
			client.send_message(bestbuy_link, title="Stock at bestbuy")
		else:
			print('No BestBuy')
		if (S.ebGames(ebGames_link)=='In Stock'):
			client.send_message(ebGames_link, title="Stock at EbGames")
		else:
			print('No EB')
		if (S.target(target_link)=='In Stock'):
			client.send_message(target_link, title="Stock at Target")
		else:
			print('No Target')
		if (S.newegg(newegg_link)=='In Stock'):
			client.send_message(newegg_link, title="Stock at Newegg")
		else:
			print('No Newegg\n\n')                                                                     
		time.sleep(refresh_time)

if __name__ == "__main__":
	main()


