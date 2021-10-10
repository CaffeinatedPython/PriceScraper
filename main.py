import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
    product_list = []

    for item in results:

        """     
        Not sure if this is an anti scraping tool or not
        Need to check if this is the money value or a random string '7S0ponso rPA Eed-1 UJ 0F -1-1'
        First pic result was returning None.
        """

        price = item.find('div', {'class', 's-item__detail s-item__detail--primary'}).text
        if '$' in price:
            price = float(price.replace('$','').replace(',', '').strip())
        pic = item.find('img', {'class', 's-item__image-img'})
        if pic is not None:
            pic = pic['src']

        title = item.find('h3', {'class', 's-item__title'}).text
        link = item.find('a', {'class', 's-item__link'})['href']

        products = {
            'title': title,
            'price': price,
            'pic': pic,
            'link': link
        }
        product_list.append(products)
    return(product_list)

def output(product_list):
    product_df = pd.DataFrame(product_list)
    print(product_df)

def main():
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=modern+horizons+2+set+booster+box&_sacat=0&LH_TitleDesc=0&_udlo=100&rt=nc&Language=English&_odkw=modern+horizons+2+booster+box&_osacat=0&LH_BIN=1&_dcat=261044&_sop=15"
    soup = get_data(url)
    output(parse(soup))



if __name__ == "__main__":
    main()