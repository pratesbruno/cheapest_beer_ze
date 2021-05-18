import streamlit as st
import json

from cheapest_beer_ze.scraper import BeerScraper

def get_cheapest_beers(address="Rua Visconde de Caravelas, 98"):
    scraper = BeerScraperV3()
    scraper.build_driver()
    scraper.define_address(address)
    scraper.get_available_brands()
    scraper.scrape_data()
    scraper.create_df()
    scraper.set_filters()
    scraper.apply_filters()
    result = scraper.filtered_df.to_json()
    return json.loads(result)

