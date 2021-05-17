import streamlit as st

from cheapest_beer_ze.utils import get_url, handle_price, get_mls, is_returnable
from cheapest_beer_ze.scraper import BeerScraper

def get_cheapest_beers():
    scraper = BeerScraper()
    print('Scraper object created.')
    scraper.build_driver()
    print('Driver built.')
    scraper.login()
    print('Login made.')
    scraper.get_available_brands()
    print(scraper.available_brands)
