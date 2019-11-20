def scrape():
    #####################################################################################
    #                                                                                   #
    # Import all the needed libraries                                                   #
    #                                                                                   #
    #####################################################################################
    from bs4 import BeautifulSoup as bs
    import requests
    import numpy
    import pandas as pd
    from splinter import Browser

    #####################################################################################
    #                                                                                   #
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph    #
    # Text. Assign the text to variables that you can reference later.                  #
    #                                                                                   #
    #####################################################################################
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_='slide')
    news_title = []
    news_p = []
    for result in results:
        news_title.append(result.find_all('div', class_='content_title')[0].find('a').text)
        news_p.append(result.find_all('div', class_='rollover_description_inner')[0].text)

    #####################################################################################
    #                                                                                   #
    # Visit the url for JPL Featured Space Image here.                                  #
    #                                                                                   #
    # Use splinter to navigate the site and find the image url for the current Featured #
    # Mars Image and assign the url string to a variable called featured_image_url.     #
    #                                                                                   #
    # Make sure to find the image url to the full size .jpg image.                      #
    #                                                                                   #
    # Make sure to save a complete url string for this image.                           #
    #                                                                                   #
    #####################################################################################
    executable_path = {'executable_path': '/drivers/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.find_by_css('a[title="Display actual size"]').click()
    featured_image_url = browser.find_by_css('img[class="fancybox-image"]')['src']

    #####################################################################################
    #                                                                                   #
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather    #
    # tweet from the page. Save the tweet text for the weather report as a variable     #
    # called mars_weather.                                                              #
    #                                                                                   #
    #####################################################################################
    url='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather = []
    for result in results:
        mars_weather.append(result.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text)
    
    #####################################################################################
    #                                                                                   #
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing   #
    # facts about the planet including Diameter, Mass, etc.                             #
    #                                                                                   #
    # Use Pandas to convert the data to a HTML table string.                            #
    #                                                                                   #
    #####################################################################################
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Fact", "Value"]
    df.set_index('Fact', inplace=True)   
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    html_table = html_table.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-striped table-sm table-condensed">')

    #####################################################################################
    #                                                                                   #
    # Visit the USGS Astrogeology site here to obtain high resolution images for each   #
    # of Mar's hemispheres.                                                             #
    #                                                                                   #
    # You will need to click each of the links to the hemispheres in order to find the  #
    # image url to the full resolution image.                                           #
    #                                                                                   #
    # Save both the image url string for the full resolution hemisphere image, and the  #
    # Hemisphere title containing the hemisphere name. Use a Python dictionary to store #
    # the data using the keys img_url and title.                                        #
    #                                                                                   #
    # Append the dictionary with the image url string and the hemisphere title to a list#
    # This list will contain one dictionary for each hemisphere.                        #
    #                                                                                   #
    #####################################################################################
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_='item')
    hemis_title = []
    hemis_url = []
    for result in results:
        hemis_title.append(result.find_all('div', class_='description')[0].find('h3').text)
    executable_path = {'executable_path': '/drivers/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    for hem in hemis_title:
        browser.click_link_by_partial_text(hem)
        response = requests.get(browser.url)
        soup = bs(response.text, 'html.parser')
        results = soup.find_all('li')
        for result in results:
            if result.find_all('a')[0].text == "Sample":
                hemis_url.append(result.find_all('a')[0]['href'])
        browser.back()
    hemisphere_image_urls = []
    for x in range (0, 4):
        myDict = {"title": hemis_title[x], "img_url": hemis_url[x]}
        hemisphere_image_urls.append(myDict)
    ret_dict = {
        "news_titles": news_title, #
        "news_paragraphs": news_p, #
        "feat_image": featured_image_url, #
        "mars_weather": mars_weather, #
        "html_table": html_table, 
        "hemis_images": hemisphere_image_urls #
    }
    
    return ret_dict