# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import pymongo

urls = {
        'news': 'https://mars.nasa.gov/news/',
        'image': 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', 
        'facts': 'https://space-facts.com/mars/',
        'hemi' :'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
}

def request_soup(url): 
    # Retrieve page 
    response = requests.get(url)
    # Create BeautifulSoup object and parse with html
    soup = BeautifulSoup(response.text, 'html.parser')
    
    return soup

# Opens up the Chrome Dash
def init_browser(): 
    # Use Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', executable_path, headless=False)

def scrape_info():


    ##########################################################
    # NASA Mars News 
    # Get title and paragraph for latest article
    # Retrieve page with the request module
    browser = init_browser()
    browser.visit(urls['news'])
    # Create BeautifulSoup Object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    slide_element = soup.select_one("ul.item_list li.slide")

    latest_news = slide_element.find("div", class_="content_title").get_text()
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()

    ##########################################################
    # JPL Mars Space Image
    # Click into the chromedriver and select Full image and more info
    browser = init_browser()
    browser.visit(urls['image'])
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    # Use Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_img = soup.find('figure', class_='lede')
    featured_img_url = f'https://www.jpl.nasa.gov{featured_img.a.img["src"]}'


    ##########################################################
    # Mars Facts
    # Use Pandas to read and scrape the table and convert to a string
    fact_table = pd.read_html(urls['facts'])

    # Create a Pandas DataFrame
    facts_df = fact_table[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index('Description', inplace=True)

    # Convert the dataframe into a html table
    html_table = facts_df.to_html()
    html_table = html_table.replace('\n', '')


    ##########################################################
    # Mars Hemispheres
    browser = init_browser()
    browser.visit(urls['hemi'])

    # Use Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the html titles and put into a list
    title = soup.find_all('div', class_='description')

    # Loop through the 'div' objects and scrape the titles and urls of images
    # Create a list to store the dictionaries
    hemis_urls = []
    for title in titled:
        # Navigate browser to page then click on title link to image page
        browser.visit(urls['hemi'])
        browser.click_link_by_partial_text(title.a.h3.text)
    
        # Grab the destination page html and make into BeautifulSoup Object
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
         # Parse the imgage source(src) relative url and then append to domain name
         # for absolute url
        img_url_list = soup.find('img', class_='wide-image')
        img_url = f"https://astrogeology.usgs.gov{img_url_list['src']}"
    
         # Create Dictionary with returned values and add dict to hemi_image_urls list
        post = {
                'title': title.a.h3.text,
                'image_url': img_url
                }
            
        hemis_urls.append(post)

    # Initialize mars_data dictionary to hold all scraped values to be entered into MongoDB
    mars_data = {
            'latest_news': latest_news, 
            'news_paragraph': news_paragraph, 
            'featured_img_url': featured_img_url,
            'html_table': html_table, 
            'hemis_urls': hemis_urls
    }
    print(mars_data)
    return mars_data
