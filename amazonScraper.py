import time
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

# Configure Selenium WebDriver
def configure_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    service = Service("C:\\webdriver\\chromedriver-win64\\chromedriver.exe")  # Replace with the path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def fetch_html_with_selenium(url):
    driver = configure_selenium()
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load
    html_content = driver.page_source
    driver.quit()
    return html_content

# Parse Product Details
def parse_product_details(product):
    try:
        name = (
            product.find("span", class_="a-size-medium a-color-base a-text-normal")
            or product.find("span", class_="a-text-normal")
            or product.find("h2")
        )
        name = name.text.strip() if name else None
    except AttributeError:
        name = None

    try:
        price = product.find("span", class_="a-price-whole")
        price = price.text.strip() if price else None
    except AttributeError:
        price = None

    try:
        rating = product.find("span", class_="a-icon-alt")
        rating = rating.text.strip() if rating else None
    except AttributeError:
        rating = None

    try:
        reviews = product.find("span", class_="a-size-base")
        reviews = reviews.text.strip() if reviews else None
    except AttributeError:
        reviews = None

    try:
        product_url = product.find("a", class_="a-link-normal")["href"]
        product_url = "https://www.amazon.com" + product_url if product_url else None
    except (AttributeError, TypeError):
        product_url = None

    try:
        image_url = product.find("img", class_="s-image")["src"]
        image_url = image_url if image_url else None
    except (AttributeError, TypeError):
        image_url = None

    return {
        "Name": name,
        "Price": price,
        "Ratings": rating,
        "Reviews": reviews,
        "Product URL": product_url,
        "Image URL": image_url,
    }

# Scrape Amazon Data
def scrape_amazon(keyword, num_pages=2):
    base_url = "https://www.amazon.com/s?k="
    products_data = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for page in range(1, num_pages + 1):
            url = f"{base_url}{keyword}&page={page}"
            futures.append(executor.submit(fetch_html_with_selenium, url))

        for future in futures:
            html_content = future.result()
            soup = BeautifulSoup(html_content, "html.parser")
            search_results = soup.find("div", class_="s-main-slot") or soup.find("div", id="search")
            
            if not search_results:
                print("No search results found.")
                continue

            products = search_results.find_all("div", {"data-component-type": "s-search-result"})
            for product in products:
                product_data = parse_product_details(product)
                if product_data["Name"]:  # Ensure we only save products with a name
                    products_data.append(product_data)

    return products_data

# Save Data to File
def save_data(data, file_format="csv"):
    if file_format == "csv":
        keys = data[0].keys()
        with open("amazon_products.csv", "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print("Data saved to amazon_products.csv")
    elif file_format == "json":
        with open("amazon_products.json", "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)
        print("Data saved to amazon_products.json")
    elif file_format == "excel":
        df = pd.DataFrame(data)
        df.to_excel("amazon_products.xlsx", index=False)
        print("Data saved to amazon_products.xlsx")
    else:
        print("Unsupported file format. Please choose csv, json, or excel.")

# Main Function
def main():
    keyword = input("Enter the product keyword to search: ")
    file_format = input("Enter the file format to save data (csv, json, excel): ").strip().lower()

    print("Scraping data... This may take some time.")
    data = scrape_amazon(keyword)

    if data:
        save_data(data, file_format)
    else:
        print("No data found for the given keyword.")

if __name__== "__main__":
    main()