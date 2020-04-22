from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import json
walmart_fruit = []
urlreq = f'https://grocery.walmart.com/v4/api/products/search?storeId=1985&query=meat&count=200&page=1&offset=0'
response = urllib.request.urlopen(urlreq)
jresponse = json.load(response)
for response in jresponse:
    res_val = jresponse[response]
    walmart_fruit.append({response: res_val})
    # print(response)
    # print(res_val)
# print(walmart_fruit)
# with open('walmart_fruits.json', 'w') as outfile:
#     json.dump(jresponse, outfile, sort_keys=True, indent=4)
# print(jresponse)
# walmart_dict = json.loads('walmart_fruits.json')
# print(walmart_dict)
UNITS = (
    ('Each', 'E'),
    ('LB', 'L'),
    ('OZ', 'O'),
    ('FL OZ', 'F'),
    ('Unit', 'U'),
    ('Gram', 'G'),
    ('KG', 'K'),
    ('GL', 'M'),
    ('Dozen', 'D')
)


def add_items(url, product_name, product_price, product_unit):
    img_url = url
    piece = ''
    products = Item.objects.filter(image=img_url)
    for product in products:
        piece = product.image
    if img_url == piece:
        pass
    else:
        img = img_url
        name = product_name
        description = name
        price = product_price
        unit = product_unit
        for idx in UNITS:
            if idx[0] == unit:
                unit = idx[1]
        item = Item(name=name, unit_price=price,
                    description=description, unit_measurement=unit, image=img)
        item.save()
produce_dict = []
prices = [2.55, 0.41, 3.46, 0.99, 3.99, 2.50, 2.00, 5.00, 3.49, 6.49, 4.99, 9.99, 34.99,
          9.99, 13.99, 27.96, 11.98, 8.50, 15.99, 4.99, 8.99, 7.49, 9.99, 2.99, 7.98, 4.29]
price_units = ["Each", "Each", "LB", "Each", "Each", "Each", "LB", "Each", "Each", "Each", "Each", "Each",
               "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each", "Each"]
urls_list = ['https://www.safeway.com/shop/product-details.184290007.html', 'https://www.safeway.com/shop/product-details.184060007.html', 'https://www.safeway.com/shop/product-details.184540027.html', 'https://www.safeway.com/shop/product-details.184450054.html', 'https://www.safeway.com/shop/product-details.184070124.html', 'https://www.safeway.com/shop/product-details.184040158.html', 'https://www.safeway.com/shop/product-details.960021862.html', 'https://www.safeway.com/shop/product-details.960015089.html', 'https://www.safeway.com/shop/product-details.196100818.html', 'https://www.safeway.com/shop/product-details.960038380.html', 'https://www.safeway.com/shop/product-details.117100189.html', 'https://www.safeway.com/shop/product-details.960078948.html', 'https://www.safeway.com/shop/product-details.960460707.html',
             'https://www.safeway.com/shop/product-details.960113677.html', 'https://www.safeway.com/shop/product-details.186190041.html', 'https://www.safeway.com/shop/product-details.960109089.html', 'https://www.safeway.com/shop/product-details.188510026.html', 'https://www.safeway.com/shop/product-details.960113679.html', 'https://www.safeway.com/shop/product-details.960275246.html', 'https://www.safeway.com/shop/product-details.960028971.html', 'https://www.safeway.com/shop/product-details.188650021.html', 'https://www.safeway.com/shop/product-details.960018494.html', 'https://www.safeway.com/shop/product-details.188100176.html?zipcode=94611', 'https://www.safeway.com/shop/product-details.960541035.html', 'https://www.safeway.com/shop/product-details.184100012.html']


def search_item(url):
    page = requests.get(url).text
    soup = bs(page, 'html.parser')
    product_name = soup.find("h2", {"class": "modal-heading"}).text.strip()
    product_img = soup.find("picture", {"class": "img-responsive"}).img['src']
    product_price = prices[urls_list.index(url)]
    product_unit = price_units[urls_list.index(url)]
    img_url = 'https:'+product_img
    produce_dict.append({'name': product_name, 'image': img_url,
                         'price': product_price, 'unit': product_unit})
for url in urls_list:
    search_item(url)
    add_items(produce_dict[urls_list.index(url)]['image'], produce_dict[urls_list.index(
        url)]['name'], produce_dict[urls_list.index(url)]['price'], produce_dict[urls_list.index(url)]['unit'])
    # print(produce_dict[urls_list.index(url)]['test'])
store_logos = []


def find_store_logo(url, selector, class_name):
    logo_url = url
    logo_page = requests.get(logo_url).text
    logo_soup = bs(logo_page, 'html.parser')
    if selector == "img":
        store_logo = logo_soup.find(selector, {"class": class_name})['src']
        store_logos.append({'src': url + store_logo})
find_store_logo("https://www.safeway.com", "img", "logo-safeway")
logo_img = store_logos[0]