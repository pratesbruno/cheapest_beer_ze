import streamlit as st
import json

from cheapest_beer_ze.scraper import BeerScraper

def get_cheapest_beers(email="brunoprates@poli.ufrj.br", password="ze123456"):
    scraper = BeerScraper()
    print('Scraper object created.')
    scraper.build_driver()
    print('Driver built.')
    scraper.login(email,password)
    print('Login made.')
    scraper.get_available_brands()
    print('Available brands retrieved.')
    #print(scraper.available_brands)
    scraper.scrape_data()
    print('Data scraped.')
    scraper.create_df()
    scraper.set_filters()
    scraper.apply_filters()
    print('Filters applied.')
    result = scraper.filtered_df.to_json()
    return json.loads(result) 

