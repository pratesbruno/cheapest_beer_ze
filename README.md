# Beer scraper - Zé Delivery
This project scrapes beer prices and other info from the brazilian delivery website "Zé Delivery", and returns the cheapest options available for the inputed address, subject to constraints defined by the user.

This project involves web scraping, text processing, creating python packages, creating an API, using Docker, deploying with Google Container and Google Cloud Run, building a front-end in Streamlit (different repo), using Pandas for some data manipulation, and finally deploying the final app in Heroku.

The front-end of this project can be found at: https://github.com/pratesbruno/cheapest_beer_frontend
The deployed app can be found at: https://cheapest-beer-ze.herokuapp.com/

## Motivation
I wanted to develop and strengthen my skills in different data-related areas, while building something useful.

The idea for this particular project came when a friend did a market research on beers. The research showed that the main factor people in their early 20s consider when
buying beer is the price. So I decided to build a tool that helps people find the cheapest beer available in their area in the most popular Brazilian beer delivery website.

Of course, looking only at the price of individual beers is misleading, because beers have different volumes - what we are really interested in is the price per ml. Also, people often have brands that they refuse to drink, or maybe they don't want 1 liter bottles because they get hot too quicky, so I decided to add those (and other) features as well.

## Project details

### Step 1 - Building the scraper
The first step was to build the scraper. This was mostly done in a jupyter notebook, that later got refactored into a python package.

There was no simple API that could be used to get all the information I wanted, so I used selelium and ChromeDriver for scraping.

In order to access the available products in the website, you either have to login to the website, or set an address. I first used the login approach, but I later decided to go for the address option to avoid dealing with sensitive information (passwords), and so users could check the prices of the beer in their region even if they do not have a Zé Delivery account.

Besides the beer and their prices, I also wanted to get the brand (which was easy), the volume of the container (which involved some Regex) and whether the beer is "returnable" or not (which means you have to give back an empty container to the deliverer in order to get a discounted price). 

To rank the cheapest beers, I used the price per mililiters. A few extra functions were included in order to create a dataframe from the results and to filter results based on user input. 
The possible filters the user can do are: 
- Filter out chosen beer brands (as some brands are considered unpalatable to some people)
- Choose a maximum size for the beer bottles/cans (bigger containers have lower price per mls, but get hot faster, so some people do not like them)
- Filter out the beers that require you to give back empty containers to the deliverer
- Define which brands they want to see (in this case, you choose the brands that you like and only those are shown - different from filtering out brands)

### Step 2 - Improving scrape time
Once the scraper was working, I realized it took over 2 minutes to run. This was far too long and most users would not like to wait all this time to get an answer on what is the cheapest beer.

I isolated the methods, measured their times, and realized a certain method was responsible for almost all that time (1m48s). This was because it was doing several get requests, one for each available brand.

As the main goal of this project is to find cheap beers, we can assume that most users won't be interested in the high-end, premium brands. So I ran an analysis to figure out the most expensive brands and excluded them. The details of the analysis can be found in the jupyter notebook.

After that, the scrape time was reduced by half.

### Step 3 - Packaging and building an API
After the scraper was working on the notebook, the code was refactored into a package.

I used FastAPI to build an API that receives the address and filters defined by the user, and returns the cheapests beers (in Price per ml).

### Step 4 - Deploying with Docker and Google Cloud Run
The API initially only worked locally, but in order to be used by other users, it had to be deployed. Docker and CG Run were used for that purpose.

There were a few challenges in this proccess. First, the API was not working with the Docker container. After a while, I realized the reason was that Chrome and the ChromeDriver were installed in my local machine only, and not in the container. This was fixed with some changes to the Dockerfile. Still, the driver kept crashing. It took some changes in the version and parameters of the driver (and a lot of time browsing StackOverflow posts) to make it all work.

After the API was running in a Docker container, I uploaded the Docker image to Google Container Registry and deployed it to Google Cloud Run. Now the API is available to anyone.

### Step 5 - Front-End
Most users do not know how to work with APIs, so I created a front-end that anyone can interact with. I created a separate project for this, so that the front-end is very light and easier to deploy on Heroku.

The front-end can be found at: https://github.com/pratesbruno/cheapest_beer_frontend
The deployed app can be found at: https://cheapest-beer-ze.herokuapp.com/
