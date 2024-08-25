import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fastapi import HTTPException
from fastapi import status as http_status
from pathlib import Path
import re
import os
import time

from database.jsonLocalDatabase import JSONStorage
from database.cache import RedisCache
from utils.ConsoleNotification import ConsoleNotification
from schema import UrlPages

class ScrapeService:
    async def scrape(urlpage: UrlPages):
        productDetailsArray = []
        exponentialBackoff = 1
        while True:
            try:
                productDetailsArray = await scrapeWebsite(urlpage.url, urlpage.pages)
                break
            except Exception as e:
                print(f"trying again with exponentialBackoff of {exponentialBackoff} seconds")
                time.sleep(exponentialBackoff)
                exponentialBackoff *= 2
                if exponentialBackoff > 8:
                    raise HTTPException(status_code=http_status.HTTP_501_NOT_IMPLEMENTED,
                                        detail=f"{e}")
                continue

        upsertProductDetailsArray = []
        cache = RedisCache()
        for product in productDetailsArray:
            title = product['product_title']
            price = product['product_price']
            if not cache.get(title):
                cache.set(title, price, ex=3600)
                upsertProductDetailsArray.append(product)
            elif float(cache.get(title).decode('utf-8')) != price:
                cache.set(title, price, ex=3600)
                upsertProductDetailsArray.append(product)
            else:
                cache.expire(title, 3600)

        for product in upsertProductDetailsArray:
            product['path_to_image'] = await saveImage(product['url'], product['product_title'])

        storage = JSONStorage(f"{os.getcwd()}/products.json")
        storage.query('upsert', upsertProductDetailsArray)

        notificationMessage = f"Scraped {len(productDetailsArray)} products from {urlpage.url} out of which {len(upsertProductDetailsArray)} were new or updated"
        ConsoleNotification.notify(message=notificationMessage)
        return notificationMessage


async def scrapeWebsite(url: str, page: int) -> list:
    productDetailsArray = []

    for page in range(page):
        html = await get_html(url)
        catelouge = html.find("div", class_="mf-shop-content")
        products = catelouge.find_all("li")
        nextPageUrl = html.find("a", class_= "next page-numbers")
        for product in products:
            img = product.find("img")
            imageUrl = img['data-lazy-src'] if img else None
            title = f"{img['alt'][:-20]}{len(imageUrl)}" if img else None

            price = product.find("span", class_="woocommerce-Price-amount amount")
            price = float(price.text[1:]) if price else 0
            if(title):
                productDetails = {
                    "url": imageUrl,
                    "path_to_image": None,
                    "product_title": title,
                    "product_price": price
                }

                productDetailsArray.append(productDetails)
        url = nextPageUrl['href']

    return productDetailsArray

async def get_html(url: str) -> BeautifulSoup:
    #disabling https verification as the website is not secure/ certificate is expired
    connector = aiohttp.TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            text = await response.text()

            if response.status == 200:
                html = BeautifulSoup(markup=text, features="lxml")

                return html

    raise HTTPException(status_code=http_status.HTTP_501_NOT_IMPLEMENTED,
                        detail=f"Scraper didn't succeed in getting data:\n"
                               f"\turl: {url}\n")

async def saveImage(url,title):
    dirToSave = Path(f"{os.getcwd()}/images")
    dirToSave.mkdir(parents=True, exist_ok=True)
    imageName = f"{re.sub(r'[^a-zA-Z0-9\s]', '', title)}.png"
    imagePath = f"{dirToSave}/{imageName}"

    #disabling https verification as the website is not secure/ certificate is expired
    connector = aiohttp.TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            image = await response.read()
            with open(imagePath, "wb") as f:
                f.write(image)

    return imagePath