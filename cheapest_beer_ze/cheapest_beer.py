import json

from cheapest_beer_ze.scraper import BeerScraper

def get_cheapest_beers(address, wb, ub, r, mm):
    scraper = BeerScraper()
    scraper.build_driver()
    scraper.define_address(address)
    if not scraper.address:
        return 'Address invalid. Please try again with a valid address.'
    scraper.get_available_brands()
    if not scraper.available_brands:
        return 'No product available now. Try again another time or with another address.'
    scraper.scrape_data()
    scraper.create_df()
    scraper.set_filters(wb,ub,r,mm)
    scraper.apply_filters()
    result = scraper.filtered_df.to_json()
    return json.loads(result)
