from bs4 import BeautifulSoup as bs
import requests

urls_list = ['https://www.safeway.com/shop/product-details.184290007.html', 'https://www.safeway.com/shop/product-details.184060007.html', 'https://www.safeway.com/shop/product-details.184540027.html',
             'https://www.safeway.com/shop/product-details.184450054.html', 'https://www.safeway.com/shop/product-details.184070124.html', 'https://www.safeway.com/shop/product-details.184040158.html', 'https://www.safeway.com/shop/product-details.960021862.html']

produce_dict = []
prices = ["$2.55/Each", "$0.41/Each", "$3.46/LB",
          "$0.99/Each", "$3.99/Each", "$2.50 /Each", "$2.00/Lb"]


def search_item(url):
    page = requests.get(url).text
    soup = bs(page, 'html.parser')
    product_name = soup.find("h2", {"class": "modal-heading"}).text.strip()
    product_img = soup.find("picture", {"class": "img-responsive"}).img['src']
    product_price = prices[urls_list.index(url)]
    produce_dict.append(
        {'name': product_name, 'image': 'https:'+product_img, 'price': product_price})


for url in urls_list:
    search_item(url)

store_logos = []


def find_store_logo(url, selector, class_name):
    logo_url = url
    logo_page = requests.get(logo_url).text
    logo_soup = bs(logo_page, 'html.parser')
    if selector == "img":
        store_logo = logo_soup.find(selector, {"class": class_name})['src']
        store_logos.append({'src': url + store_logo})
    else:
        store_logo = logo_soup.find(selector, {"class": class_name}).svg
        store_logos.append({'svg': store_logo})


find_store_logo("https://www.safeway.com", "img", "logo-safeway")
find_store_logo("https://www.target.com", "a", "Link-sc-1khjl8b-0")

logo_img = store_logos[0]
logo_svg = store_logos[1]
