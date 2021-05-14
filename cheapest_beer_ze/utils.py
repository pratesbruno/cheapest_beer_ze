import re
import numpy as np
from unidecode import unidecode

# This function creates the url string for a particular brand
def get_url(brand):
    root_url = 'https://www.ze.delivery/produtos/marca/'
    brand = brand.lower()
    brand = unidecode(brand)
    brand = brand.replace("'", "")
    brand = brand.replace(" ", "-")
    return root_url+brand

# This function takes the price in the format that it is found in the HTML, and convert to a float.
def handle_price(price):
    price = price.text[3:]
    price = price.replace(',','.')
    return float(price)

# This function get the number of mls in a product
def get_mls(product):
    pattern1 = r"(\d+)ml"
    pattern2 = r"(\d*\.*\d+)L"
    try:
        ml = float(re.findall(pattern1, product)[0])
    except:
        try:
            ml = int(float(re.findall(pattern2, product)[0])*1000)
        except:
            ml = np.nan
    return ml

# This function checks if the product is returnable, by looking at its name
def is_returnable(product):
    if product.find('Apenas o ') == -1:
        return 'No'
    return 'Yes'