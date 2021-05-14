# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)
    news_title, news_p = mars_news(browser)
    data = {
        "news_title":news_title, 
        "news_p":news_p,
        "featured_image":featured_image(browser),
        "mars_facts":mars_facts(browser),
        "mars_hemisphere":mars_hemisphere(browser)
    }
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

def mars_facts(browser):
    # Use `pd.read_html` to pull the data from the Mars-Earth Comparison section
    df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    df.columns=['Description', 'Mars','Earth']
    df.set_index('Description', inplace=True)
    df.to_html()
    return df.to_html(classes = "table-striped table")

def mars_hemisphere(browser):
    # 1. Use browser to visit the URL 
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    all_links = browser.find_by_css("a.product-item img")
    for link in range(len(all_links)):
        hemisphere = {}
        browser.find_by_css("a.product-item img")[link].click()
        hemisphere["title"] = browser.find_by_css("h2.title").text
        link_elements = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = link_elements["href"]
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls

if __name__=="__main__":
    print(scrape_all())