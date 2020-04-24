from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item, Store
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import json

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
store_logos = []


def find_store_logo(url, selector, class_name):
    logo_url = url
    logo_page = requests.get(logo_url).text
    logo_soup = bs(logo_page, 'html.parser')
    if "safeway" in url:
        store_logo = logo_soup.find(selector, {"class": class_name})['src']
        store_name = logo_soup.title.text[-7:]
        store_logos.append({'src': url + store_logo, 'store_name': store_name})
    else:
        store_logo = 'i5.walmartimages.com/dfw/63fd9f59-43e0/1ed7036a-feba-43ca-8885-1d937a9aa4f2/v1/spark-yellow-spark.b43cc07989a08d84d33b0c87dd8afb1998431e48.svg'
        store_name = logo_soup.title.text[:7]
        store_logos.append({'src': store_logo, 'store_name': store_name})


stores_url = ['https://www.safeway.com', 'https://www.walmart.com/']

for url in stores_url:
    if "safeway" in url:
        find_store_logo(url, "img", "logo-safeway")
    # elif url != None:
    #     find_store_logo(url, "div", "al_b")

logo_img = store_logos
st_name = []
for st in store_logos:
    st_name.append(st['store_name'])
stores = None
if Store.objects.filter(name=st_name[0]):
    stores = Store.objects.filter(name=st_name[0])
else:
    for store in store_logos:
        st_store = Store(name=store['store_name'], image=store['src'])
        st_store.save()

stores = Store.objects.filter(name=st_name[0])
# print(st_name)
# print(stores.first().id)


walmart_fruit = []
urlreq = f'https://grocery.walmart.com/v4/api/products/search?storeId=1985&query=meat&count=50&page=1&offset=0'
response = urllib.request.urlopen(urlreq)

jresponse = json.load(response)


def add_walmart_item(products):
    product_list = []
    for food in products:
        alive = food
        if alive:
            unit = 'E'+food['store']['price']['priceUnitOfMeasure'][1:]
            for idx in UNITS:
                if idx[0] == unit and unit != None:
                    unit = idx[1]
            product_list.append({'img_url': food['basic']['image']['thumbnail'], 'name': food['basic']['name'][:100],
                                 'price': food['store']['price']['list'], 'unit': unit[:1], 'counts': food['store']['price']['salesQuantity']})
    piece = ''
    for item in product_list:
        products = Item.objects.filter(image=item['img_url'])
        # print(img['img_url'])
        for product in products:
            piece = product.image
        if piece == item['img_url']:
            # print(piece)
            pass
        else:
            description = item['name']
            stores = Store.objects.filter(name=st_name[1])
            # print(item['name'])
            item = Item(name=item['name'], unit_price=item['price'], item_count=item['counts'],
                        description=description, unit_measurement=item['unit'], image=item['img_url'], store=stores.first())
            item.save()


add_walmart_item(jresponse['products'])


def add_items(url, product_name, product_price, product_unit, product_count):
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
        counts = product_count
        price = product_price
        stores = Store.objects.filter(name=st_name[0])
        unit = product_unit
        for idx in UNITS:
            if idx[0] == unit:
                unit = idx[1]

        item = Item(name=name, unit_price=price,
                    description=description, unit_measurement=unit, image=img, item_count=counts, store=stores.first())
        item.save()


produce_dict = []
prices = [2.55, 0.41, 3.46, 0.99, 3.99, 2.50, 2.00, 5.00, 3.49, 6.49, 4.99, 9.99, 34.99,
          9.99, 13.99, 27.96, 11.98, 8.50, 15.99, 4.99, 8.99, 7.49, 9.99, 2.99, 7.98, 4.29]
counts = [2, 41, 34, 99, 39, 25, 20, 50, 34, 64, 99, 199, 89,
          79, 139, 96, 98, 85, 15, 59, 9, 74, 16, 29, 78, 42]
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
    product_count = counts[urls_list.index(url)]
    product_unit = price_units[urls_list.index(url)]
    img_url = 'https:'+product_img
    produce_dict.append({'name': product_name, 'image': img_url,
                         'price': product_price, 'unit': product_unit, 'count': product_count})


for url in urls_list:
    search_item(url)
    add_items(produce_dict[urls_list.index(url)]['image'], produce_dict[urls_list.index(
        url)]['name'], produce_dict[urls_list.index(url)]['price'], produce_dict[urls_list.index(url)]['unit'], produce_dict[urls_list.index(url)]['count'])
    # print(produce_dict[urls_list.index(url)]['test'])
