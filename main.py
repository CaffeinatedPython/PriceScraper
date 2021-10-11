import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests


import unicodedata

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse_ebay(soup):
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
    product_list = []
    now = datetime.now().strftime("%Y%m%d")

    for item in results:

        """     
        Not sure if this is an anti scraping tool or not
        Need to check if this is the money value or a random string '7S0ponso rPA Eed-1 UJ 0F -1-1'
        First pic result was returning None.
        """

        price = item.find('div', {'class', 's-item__detail s-item__detail--primary'}).text
        if '$' in price:
            price = float(price.replace('$','').replace(',', '').strip())
        else:
            continue
        pic = item.find('img', {'class', 's-item__image-img'})
        if pic is not None:
            pic = pic['src']

        title = item.find('h3', {'class', 's-item__title'}).text
        link = item.find('a', {'class', 's-item__link'})['href']

        products = {
            'title': title,
            'price': price,
            'pic': pic,
            'link': link,
            'date' : now
        }
        product_list.append(products)
    return(product_list)


def parse_mtggoldfish(soup):
    #results = soup.find('div', {'class', 'price-card-purchase price-card-purchase-mobile'})
    results = soup.find_all('a')

    '''
    There is a second tag at the bottom of the page that causes this to run twice.

    '''
    product_list = []
    now = datetime.now().strftime("%Y%m%d")
    for each in results:
        #wanted something more elegant than 2 if statements but nothing
        #I tried was getting rid of the dupes
        if 'Market Price' in each.text:
            #strip output for price
            print(each.text)

        elif 'eBay - ' in each.text:
            if 'eBay' in each.text:
                #strip output for price
                print(each.text)
                #isolating for testing
                ebay_tester = each.text




    #will... not... get... rid... of... dead.... space...WTF
    print(ebay_tester.rstrip().lstrip().strip())

    #this is for formatting in a future step
    title = ''
    price = ''
    pic = ''
    link = ''

    #future formating
    products = {
        'title': title,
        'price': price,
        'pic': pic,
        'link': link,
        'date' : now
    }
    product_list.append(products)
    return(product_list)

def output(product_list):
    product_df = pd.DataFrame(product_list)
    print(product_df)

def main():

    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=modern+horizons+2+set+booster+box&_sacat=0&LH_TitleDesc=0&_udlo=100&rt=nc&Language=English&_odkw=modern+horizons+2+booster+box&_osacat=0&LH_BIN=1&_dcat=261044&_sop=15"
    name = "Modern Horizons 2"
    soup = get_data(url)
    product_list = parse_ebay(soup)
    #print(to_json(product_list, name))


    url = 'https://www.mtggoldfish.com/price/Adventures+in+the+Forgotten+Realms/Adventures+in+the+Forgotten+Realms+Draft+Booster+Box-sealed#paper'
    name = "Adventures in the Forgotten Realms Draft Booster Box"
    goldfish_soup = get_data(url)
    #print(goldfish_soup)
    product_list = parse_mtggoldfish(goldfish_soup)
    #print(product_list)




def to_json(product_list, name):
    format_json = {name: product_list}
    return(json.dumps(format_json))

if __name__ == "__main__":
    main()