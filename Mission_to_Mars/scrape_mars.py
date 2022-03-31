from cgitb import text
from inspect import Attribute
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_teaser = mars_news(browser)
    img_url_titles = mars_hemis(browser)

    data = {
        'news_title': news_title,
        'news_teaser': news_teaser,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': img_url_titles,
    }

    browser.quit
    return data


def mars_news(browser):
    # Visit the website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest Mars news
    news_title = soup.find('div', class_='content_title').text
    news_teaser = soup.find('div', class_='article_teaser_body').text
    return news_title, news_teaser


def featured_image(browser):
    # Visit the website
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Get the featured image
    full_image = browser.find_by_tag('button')[1]
    full_image.click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        img_url = soup.find('img', class_="fancybox-image").get('src')
    except AttributeError:
        return None

    feat_img_url = f'https://spaceimages-mars.com/{img_url}'
    return feat_img_url


def mars_facts():
    # Get the Mars facts table
    try:
        df = tables = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException: 
        return None
    
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()


def mars_hemis(browser):
    # Visit the website
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Get the Mars hemipshere pictures and their names
    hemisphere_image_urls = []

    for hemis in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        
        # Scrape page into Soup
        html = browser.html
        hemi_soup = bs(html, 'html.parser')

        title = hemi_soup.find('h2', class_ = 'title').text
        img_url = hemi_soup.find('li').a.get('href')
        
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    
    return hemisphere_image_urls

    
if __name__ == "__main__":
    print(scrape_all())