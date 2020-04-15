from bs4 import BeautifulSoup as bs
import requests

urls_list = ['https://www.safeway.com/shop/product-details.184290007.html', 'https://www.safeway.com/shop/product-details.184060007.html', 'https://www.safeway.com/shop/product-details.184540027.html', 'https://www.safeway.com/shop/product-details.184450054.html', 'https://www.safeway.com/shop/product-details.184070124.html', 'https://www.safeway.com/shop/product-details.184040158.html', 'https://www.safeway.com/shop/product-details.960021862.html', 'https://www.safeway.com/shop/product-details.960015089.html', 'https://www.safeway.com/shop/product-details.196100818.html', 'https://www.safeway.com/shop/product-details.960038380.html', 'https://www.safeway.com/shop/product-details.117100189.html', 'https://www.safeway.com/shop/product-details.960078948.html', 'https://www.safeway.com/shop/product-details.960460707.html', 'https://www.safeway.com/shop/product-details.960156272.html', 'https://www.safeway.com/shop/product-details.186190041.html', 'https://www.safeway.com/shop/product-details.960109089.html', 'https://www.safeway.com/shop/product-details.188510026.html', 'https://www.safeway.com/shop/product-details.960113679.html', 'https://www.safeway.com/shop/product-details.960275246.html', 'https://www.safeway.com/shop/product-details.960028971.html']

produce_dict = []
prices = ["$2.55/Each", "$0.41/Each", "$3.46/LB", "$0.99/Each", "$3.99/Each", "$2.50 /Each", "$2.00/Lb", "$5.00", "$3.49", "$6.49", "$4.99", "$9.99", "$34.99", "$8.99", "$13.99", "$27.96", "$11.98", "This item is not available right now", "$15.99", "$4.99"]

def search_item(url):
  page = requests.get(url).text
  soup = bs(page, 'html.parser')
  product_name = soup.find("h2", {"class": "modal-heading"}).text.strip()
  product_img = soup.find("picture", {"class": "img-responsive"}).img['src']
  product_price = prices[urls_list.index(url)]
  produce_dict.append({'name': product_name, 'image': 'https:'+product_img, 'price': product_price})

for url in urls_list:
  search_item(url)

store_logos = []

# url_wf = 'https://www.amazon.com/s?i=wholefoods&bbn=18473610011&rh=n%3A21121954011&pf_rd_p=0e7f104a-11fb-4088-9de1-e95d08d908c4&pf_rd_r=MXBGNT2Q1SNC7GEJAE47&ref=wf_dsk_mrk_mw_sml_WF000304'

# def whole_food(url):
#   page = requests.get(url).text
#   soup = bs(page, 'html.parser')
#   product_name = soup.select("div", attr={"class": "s-image-square-aspect"})
#   product_img = soup.find("div", {"class": "aok-relative"})
#   print(product_name) #+ " " + product_img)

# whole_food(url_wf)

# url_w = 'https://shop.wegmans.com/product/49557/wegmans-clementines'

# def wegmans(url_w):
#     page = requests.get(url).text
#     soup = bs(page, 'html.parser')
#     product_name = soup.find("div", {"class": "product-info"})
#     product_img = soup.find("div", {"class": "product-image"})
#     # product_price = soup.find("span", {"class": "css-1o7wxo5"}).img['src']
#     print(product_name) #+ " " + product_img)
    
# wegmans(url_w)

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