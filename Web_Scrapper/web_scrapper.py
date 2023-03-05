import urllib.request as urllib2
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import shelve

class WebScrapper():
    
    def __init__(self,  dbname):
        self.root_wp = 'http://books.toscrape.com/index.html'
        self.root_soup = self.get_soup(self.root_wp)
        self.get_categories()
        self.create_db(dbname)


    def get_soup(self, webpage):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        request = urllib2.Request(webpage, headers=hdr)
        my_url = urllib2.urlopen(request)
        soup = BeautifulSoup(my_url.read(), 'html.parser')
        return soup

    def get_categories(self):
        links = self.root_soup.find_all(href=re.compile('category'))

        clean_links = {}
        for link in links:
            #print(link.get('href'))
            full_link = urljoin(self.root_wp, link.get('href'))
            found = re.search(r'(books/)(.+)(/)', full_link)
            if found:
                name = found.group(2)
                clean_links[name] = full_link

        self.categories = clean_links
    
    def parse(self):
        for category_name, category_link in self.categories.items():
            """print("Performing Category: {} with link {}".format(
                category_name, category_link))"""
            soup = self.get_soup(category_link)
            self.prices[category_name] = self.get_prices_stars(soup, category_link)
        self.close_db()



    def get_prices_stars(self, soup, link):
        prices = []
        products = soup.find_all(class_=re.compile('product_pod'))
        text_to_num = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

        for p in products:
            item = p.find('h3')
            book_url = urljoin(link, item.a.get('href'))
            
            name = item.string
            price = p.find(class_="price_color").string
            clean_price = (float(re.sub(r'£', '', price)))
            
            rating = text_to_num[p.find(
                class_=re.compile("rating"))['class'][1]]
            prices.append(
                {'Name': str(name), 'Rating': rating, 'Price': clean_price, 'URL': book_url})
        return prices

    def create_db(self, name):
        self.prices = shelve.open(name, writeback=True, flag='c')

    def close_db(self):
        self.prices.close()
