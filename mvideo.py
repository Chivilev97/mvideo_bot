import requests


cookies = {'MVID_CITY_ID': 'CityCZ_975', 'MVID_REGION_ID': '1', 'MVID_REGION_SHOP': 'S002', 'MVID_TIMEZONE_OFFSET': '3'}


def get_product(product_id):
    url_name = f'https://www.mvideo.ru/bff/product-details?productId={product_id}'
    url_price = f'https://www.mvideo.ru/bff/products/prices?productIds={product_id}&isPromoApplied=true&addBonusRubles=true'
    response_price = requests.get(url=url_price, cookies=cookies).json()
    response = requests.get(url=url_name, cookies=cookies).json()
    article = response['body']['productId']
    name = response['body']['name']
    price = response_price['body']['materialPrices'][0]['price']['salePrice']
    product_url = f'https://www.mvideo.ru/products/{article}'
    return {'article': article, 'name': name, 'price': price, 'product_url': product_url}


def get_price(product):
    url_price = product[5]
    response_price = requests.get(url=url_price, cookies=cookies).json()
    return response_price['body']['materialPrices'][0]['price']['salePrice']
