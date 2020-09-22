#Web Scraping Challenge
#This is the major scrape data for the app.py the main functions are in app.py
# Dependencies
#NASA Mars News Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.
import os
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scraper(): 
    browser=init_browser()

#Visit the url for JPL Featured Space Image here.   
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    element = soup.find('ul', class_= "item_list")
   
    newsTitle = element.find("div", class_="content_title").get_text()
    paragText = element.find("div", class_="article_teaser_body").get_text()
    
    # finding the button for splinter to click taking it to the full image html
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    #splinter is finding the button with browser.find by the id "full_image then clicking the button
    button = browser.find_by_id("full_image")
    button.click()
    
    #splinter is finding the next button with browser.find_by_partial_text "full_image then clicking the button

    browser.is_element_present_by_text('more info', wait_time=1)
    button2 = browser.links.find_by_partial_text("more info")
    button2.click()

    #featured_image_url = ""
    html = browser.html
    image_soup = BeautifulSoup(html,"html.parser")
    image_soup
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    fImage = soup.find('figure', class_= "lede")
    #print(fImage)

    image_url = fImage.find("a").get("href")
    print(image_url)

    full_url = "https://www.jpl.nasa.gov" + image_url
    print(full_url)
    
    #Mars Facts¶
#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
#including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars'
    
    tables = pd.read_html(url)
    tables
    
    type(tables)
    
    df = tables[0]
    df.head()
    
    html_table = df.to_html()
    html_table
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []
    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")
    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        # Finally, we navigate backwards
        browser.back()
        
    hemisphere_image_urls
    
    data={
     "newstitle": newsTitle, 
     "paragraph": paragText,
     "feature": full_url,
     "facts": html_table,
     "hemispheres": hemisphere_image_urls
    }
    return data

