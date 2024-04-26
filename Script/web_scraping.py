# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:51:31 2024

@author: keneo
"""

import pandas as pd
import requests
import bs4

# Request url
url = 'https://books.toscrape.com'

# Retrieve the website
page = requests.get(url)
soup = bs4.BeautifulSoup(page.text, 'html.parser')

# Create lists where the scraped data will be stored
page_link = []
title = []
rating = []
price = []
stock_availability = []
upc = []
quantity = []
category = []

# (A.) Question: Collect 1000 (or as many as possible) items from the website and 
#                save them to csv(s) files.

# Create a loop to go through each page
for i in range(1, 51):
    
    # Append each page to a list
    page_link.append(f"{url}/catalogue/category/books_1/page-{i}.html")
    
# Create a loop to go through the list of links
for url2 in page_link:

    page2 = requests.get(url2)
    soup2 = bs4.BeautifulSoup(page2.text, 'html.parser')
    
    # Create a loop to find the links to all the books 
    link_all = soup2.find_all('article', {'class':'product_pod'})
    
    for details in link_all:
        link = details.find('h3').a['href'].replace('../../', 'https://books.toscrape.com/catalogue/')
        page3 = requests.get(link)
        soup3 = bs4.BeautifulSoup(page3.text, 'html.parser')
        
    # 1.) Title
    # Scrap all the book titles from the website
        title2 = soup3.find_all('h1')
        title.append(title2[0].text)
        
    # 2.) Rating
    # Scrap all the book ratings from the website
        rating2 = soup3.find_all('p')
        rating.append(rating2[2].attrs['class'][1])
        
    # 3.) Price
    # Scrap all the book prices from the website
        price2 = soup3.find_all('p')
        price.append(price2[0].text.replace('Â£',''))
        
    # 4.) Stock availability (Boolean)
    # Scrap all book stock availabilities from the website and represent them in boolean
        stock_availability2 = soup3.find_all('td')
        stock_availability3 = ' '.join(stock_availability2[5].text.split()[:2])
        in_stock = 'In stock' in stock_availability3
        stock_availability.append(in_stock)
    
    # 5.) UPC
    # Scrap all the book UPC's from the website
        upc2 = soup3.find_all('td')
        upc.append(upc2[0].text)
    
    # 6.) Quantity available
    # Scrap all the book quantities available from the website
        quantity2 = soup3.find_all('td')
        quantity.append(' '.join(quantity2[5].text.split()[-2:]).replace('(','').replace(')',''))
    
    # 7.)  Category
    # Scrap all the book categories from the website
        category2 = soup3.find_all('a')
        category.append(category2[3].text)
    
    # Print all the scraped data
    print(title)
    print(rating)
    print(price)
    print(stock_availability)
    print(upc)
    print(quantity)
    print(category)
    
# Create a dataframe to store the data
books = pd.DataFrame({'Title': title,
                          'Rating': rating,
                          'Price': price,
                          'Stock availability': stock_availability,
                          'UPC': upc,
                          'Quantity': quantity,
                          'Category': category})

# Save the dataframe to a csv file
books.to_csv(r'scraped_books_data.csv', index = False)