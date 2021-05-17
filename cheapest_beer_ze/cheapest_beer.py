import streamlit as st
import json

from cheapest_beer_ze.scraper import BeerScraper

def get_cheapest_beers(email="brunoprates@poli.ufrj.br", password="ze123456"):
    scraper = BeerScraper()
    scraper.build_driver()
    scraper.login(email,password)
    if scraper.login_status == 'Failed':
        return 'Login failed. Please try again.'
    scraper.get_available_brands()
    scraper.scrape_data()
    scraper.create_df()
    scraper.set_filters()
    scraper.apply_filters()
    result = scraper.filtered_df.to_json()
    return json.loads(result) 

