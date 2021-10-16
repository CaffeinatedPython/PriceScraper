import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse_ebay(soup):
    """
    Returns the 3 lowest priced auctions sorted as a list of dict
    """
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

    #Sort for 3 lowest prices
    sorted_product_list = sorted(product_list, key = lambda i: (i['price']))[:3]



    return(sorted_product_list)


def parse_mtggoldfish(soup, name, link):

    results = soup.find_all('a')

    '''
    There is a second tag at the bottom of the page that causes this to run twice.
    '''
    product_list = []
    now = datetime.now().strftime("%Y%m%d")
    for each in results:

        if 'Market Price' in each.text:
            tcg_price = float(each.text.strip().replace('\n', '').split('$', 1)[1].strip())

        elif 'eBay - ' in each.text:
            if 'eBay' in each.text:
                ebay_price = float(each.text.strip().replace('\n', '').split('$', 1)[1].strip())

    picture = soup.find_all('picture')
    for each in picture:
        image = each.find('img')
        pic = image['src']

    #future formating
    products = {
        'title': name,
        'price': sorted([ebay_price,tcg_price])[0],
        'pic': pic,
        'link': link,
        'date' : now
    }




    return(products)

def output(product_list):
    product_df = pd.DataFrame(product_list)
    print(product_df)

def generate_markdown(json_data):
    markdown = {}

    for game in json_data:
        markdown[game] = []
        for product in json_data[game]:
            soup = ''
            if 'ebay' in product:
                soup = get_data(product['ebay'])
                ebay = parse_ebay(soup)
                #Taking lowest ebay price
                markdown[game].append(ebay[0])

            if 'mtggoldfish' in product:
                soup = get_data(product['mtggoldfish'])
                mtggoldfish = parse_mtggoldfish(soup, product['name'], product['mtggoldfish'])
                markdown[game].append(mtggoldfish)

    #print(markdown)

    return(markdown)

def create_page(markdown):


    header = ("---\n"
                "layout: page\n"
                "---\n"
              )
    table_start =(
                "|Pic|Name|Price|\n"
                "|:-:|---|---|\n")


    all_tables = []
    for game in markdown:
        table = table_start
        boxes = ''
        for product in markdown[game]:
            line = '| <img src=\"' + product['pic'] + '\" width=\"75\" height=\"75\"> | <a href=\"' + product['link'] + '\">' + product['title'] + ' | $' + str(product['price']) + ' |\n'
            boxes += line
        table += boxes
        all_tables.append(table)


    page = header + '\n'.join(all_tables)

    return(page)


def write_page(file_name, page):
    f = open(file_name, 'w')
    f.write(page)
    f.close()


def read_json(file_name):
    f = open(file_name)
    data = json.load(f)

    f.close()
    return(data)


def main():


    file_name = "products.json"
    json_data = read_json(file_name)

    markdown = generate_markdown(json_data)
    page = create_page(markdown)

    write_page("prices.md", page)





    #url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=modern+horizons+2+set+booster+box&_sacat=0&LH_TitleDesc=0&_udlo=100&rt=nc&Language=English&_odkw=modern+horizons+2+booster+box&_osacat=0&LH_BIN=1&_dcat=261044&_sop=15"
    #name = "Modern Horizons 2"
    #soup = get_data(url)
    #product_list = parse_ebay(soup)
    #print(to_json(product_list, name))

    #url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=tales+of+aria+first+edition+booster+box+-%28bundle%2C+repack*%2C+break%2C+case%2C+opened%2C+pack*%2C+empty%2C+lot%2C+raffle%2C+theme%2C+Chinese%2C+French%2C+German%2C+Italian%2C+Korean%2C+Japanese%2C+Portuguese%2C+Russian%2C+Spanish%2C+deutsch%29&_sacat=0&LH_TitleDesc=0&_odkw=tales+of+aria+first+edition+booster+box&_osacat=0&LH_BIN=1&_sop=15"
    #name = "Tales of Aria - Booster Box First Edition"
    #$soup = get_data(url)
    #product_list = parse_ebay(soup)
    #print(to_json(product_list, name))


    #url = 'https://www.mtggoldfish.com/price/Adventures+in+the+Forgotten+Realms/Adventures+in+the+Forgotten+Realms+Draft+Booster+Box-sealed#paper'
    #name = "Adventures in the Forgotten Realms Draft Booster Box"
    #goldfish_soup = get_data(url)
    #product_list = parse_mtggoldfish(goldfish_soup, name)
    #print(product_list)
    #print(to_json(product_list, name))




def to_json(product_list, name):
    format_json = {name: product_list}
    return(json.dumps(format_json))

if __name__ == "__main__":
    main()