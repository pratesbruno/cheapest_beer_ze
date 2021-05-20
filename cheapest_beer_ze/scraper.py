import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np
from cheapest_beer_ze.utils import get_url, handle_price, get_mls, is_returnable


class BeerScraper:
    def __init__(self):
        self.driver = None
        self.email = None
        self.password = None
        self.login_status = None
        self.address = None
        self.available_brands = []
        self.prices = []
        self.products = []
        self.brands = []
        self.df = None
        self.expensive_brands = ['Cervejaria Bohemia','Hoegaarden','Farra Bier','Patagonia','Noi','Flamingo','Wäls','Motim',
                                 'Goose Island','Kona','Overhop','Hocus Pocus','Leffe','Three Monkeys','Franziskaner']
        # Filters
        self.wanted_brands = []
        self.unwanted_brands = []
        self.returnable = ['Yes','No']
        self.max_mls = 99999
        self.filtered_df = None
        
    def build_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        print('Driver built.')

        # options = webdriver.ChromeOptions()
        # options.binary_location = '/app/.apt/usr/bin/google-chrome'
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--disable-notifications")
        # options.add_argument('--headless')
        # browser = webdriver.Chrome(executable_path=chrome_location, chrome_options=options)
    
    def login(self, email, password):
        # Login details
        login_url = 'https://www.ze.delivery/conta/entrar'
        self.email = email
        self.password = password

        # Enter login details in form
        self.driver.get(login_url)
        self.driver.find_element_by_xpath("""//*[@id="login-mail-input-email"]""").send_keys(self.email)
        self.driver.find_element_by_xpath("""//*[@id="login-mail-input-password"]""").send_keys(self.password)

        # Press sign in button
        button = self.driver.find_element_by_xpath("""//*[@id="login-mail-button-sign-in"]""")
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(3) # Wait a couple seconds to complete the sign in
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        user_badger = soup.find_all("div", class_="css-1p15ya-userBadgeBase")
        if len(user_badger) > 0:
            print('Login successful.')
            self.login_status = 'Success'
        else:
            print('Login failed.')
            self.login_status = 'Failed'
    
    def define_address(self,address):
        
        login_url = 'https://www.ze.delivery'
        self.driver.get(login_url)
        try:
            # Click "over 18 years" button
            self.driver.find_element_by_xpath("""//*[@id="age-gate-button-yes"]""").click()
            # Click fake address input to reveal true address input
            self.driver.find_element_by_xpath("""//*[@id="fake-address-search-input"]""").click()
            # Fill address input with the provided address
            self.driver.find_element_by_xpath("""//*[@id="address-search-input-address"]""").send_keys(address)
            # Choose the first address from the google Autocomplete address (Check how to make this more robust later)
            self.driver.find_element_by_xpath("""//*[@class="css-bk3xhj-container-googleAutocompleteCard-AutoCompleteAddressListItem"][1]""").click()
            # Choose any complement for the address, as it won't make a difference on the available beers
            self.driver.find_element_by_xpath("""//*[@id="address-details-input-complement"]""").send_keys('1')
            # Click the button to send info to the website and continue
            self.driver.find_element_by_xpath("""//*[@id="address-details-button-continue"]""").click()
            # Wait 3 seconds for the website to proccess the information
            time.sleep(3)
            self.address = address
            print('Address set.')
        except:
            print('Failed to set address. Please try again.')

    def get_available_brands(self):
        print(1)
        url_brands = 'https://www.ze.delivery/produtos/categoria/cervejas'
        self.driver.get(url_brands) # ERRO AQUI
        print(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        available_brands_html = soup.find_all("h2", class_="css-l9heuk-shelfTitle")
        print(3)
        self.available_brands = [brand_html.text for brand_html in available_brands_html]
        print('Available brands retrieved.')
        
    def scrape_data(self):
        for brand in self.available_brands:
            if brand not in self.expensive_brands:
                #Get page HTML
                url = get_url(brand)
                self.driver.get(url)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                #Find products and add to instance variable
                products_html = soup.find_all("h3", class_="css-krg860-productTitle")
                for product in products_html:
                    self.products.append(product.text)

                #Find prices and add to instance variable.
                prices_html = soup.find_all("div", class_="css-t89dhz-priceText")
                for price in prices_html:
                    self.prices.append(handle_price(price))
                    self.brands.append(brand) # Leverage the for loop to include brand names
        print('Data scraped.')

    def create_df(self):
        self.df = pd.DataFrame(list(zip(self.products,self.prices,self.brands)),columns=['Product','Price','Brand'])
        self.df['Mls'] = self.df['Product'].map(get_mls)
        self.df['Price Per Liter'] = self.df['Price']/self.df['Mls']*1000
        self.df['Returnable'] = self.df['Product'].map(is_returnable)
        # Sort
        self.df = self.df.sort_values('Price Per Liter')
    
    def set_filters(self,wb=[],ub=[],r=['Yes','No'],mm=99999):
        self.wanted_brands = wb
        self.unwanted_brands = ub
        self.returnable = r
        self.max_mls = mm
        
    def apply_filters(self):
        # Conditions
        c0 = self.df['Brand'].isin(self.wanted_brands) if len(self.wanted_brands)>0 else self.df['Brand']==self.df['Brand']
        c1 = np.logical_not(self.df['Brand'].isin(self.unwanted_brands))
        c2 = self.df['Returnable'].isin(self.returnable)
        c3 = self.df['Mls']<=self.max_mls
        combined_cond = c0&c1&c2&c3
        # Apply condition
        self.filtered_df = self.df[combined_cond]
        self.filtered_df.reset_index(drop=True,inplace=True)
        print('Filters applied.')