import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np

class BeerScraper:
    def __init__(self):
        self.driver = None
        self.email = None
        self.password = None
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
        self.driver = webdriver.Chrome(options=options)
    
    def login(self):
        # Login details
        login_url = 'https://www.ze.delivery/conta/entrar'
        self.email = "brunoprates@poli.ufrj.br" ############### Mudar depois
        self.password = "ze123456"
        
        # Enter login details in form
        self.driver.get(login_url)
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_xpath("""//*[@id="login-mail-input-email"]""").send_keys(self.email)
        self.driver.find_element_by_xpath("""//*[@id="login-mail-input-password"]""").send_keys(self.password)

        # Press sign in button
        button = self.driver.find_element_by_xpath("""//*[@id="login-mail-button-sign-in"]""")
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(3) # Wait a couple seconds to complete the sign in
        
    def get_available_brands(self):
        url_brands = 'https://www.ze.delivery/produtos/categoria/cervejas'
        self.driver.get(url_brands)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        available_brands_html = soup.find_all("h2", class_="css-l9heuk-shelfTitle")
        self.available_brands = [brand_html.text for brand_html in available_brands_html]
        
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
        