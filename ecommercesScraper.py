import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_amazon_data(url):
    """
    Scrapes product title and price from an Amazon product page using Selenium with Microsoft Edge.
    """
    options = Options()
    # Uncomment the next line to run headless once debugging is complete
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get(url)
    print("🔄 Loading Amazon product page...")
    time.sleep(5)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)
    wait = WebDriverWait(driver, 20)

    title = None
    title_selectors = [
        {"by": By.ID, "value": "productTitle"},
        {"by": By.XPATH, "value": "//span[@id='productTitle']"},
        {"by": By.XPATH, "value": "//h1[@id='title']"}
    ]
    for selector in title_selectors:
        try:
            title_element = wait.until(EC.presence_of_element_located((selector["by"], selector["value"])))
            title = title_element.text.strip()
            if title:
                print(f"✅ Amazon Title found using {selector}")
                break
        except Exception as e:
            print(f"⚠️ Amazon Title not found with selector {selector}: {e}")
    if not title:
        title = "Amazon Title not found"

    price = None
    price_selectors = [
        {"by": By.ID, "value": "priceblock_ourprice"},
        {"by": By.ID, "value": "priceblock_dealprice"},
        {"by": By.XPATH, "value": "//*[@id='priceblock_ourprice']"},
        {"by": By.XPATH, "value": "//*[@id='priceblock_dealprice']"},
        {"by": By.XPATH, "value": "//span[contains(@class, 'a-price-whole')]"}
    ]
    for selector in price_selectors:
        try:
            price_element = wait.until(EC.presence_of_element_located((selector["by"], selector["value"])))
            price_text = price_element.text.strip()
            if price_text:
                # Remove currency symbols and formatting
                price = price_text.replace("₹", "").replace("$", "").replace(",", "").strip()
                print(f"✅ Amazon Price found using {selector}")
                break
        except Exception as e:
            print(f"⚠️ Amazon Price not found with selector {selector}: {e}")
    if not price:
        price = "Amazon Price not found"

    amazon_data = {"Title": title, "Price": price}
    driver.quit()
    return amazon_data

def get_meesho_data(url):
    """
    Scrapes product title and price from a Meesho product page using Selenium with Microsoft Edge.
    """
    options = Options()
    # Uncomment the next line for headless mode once debugging is complete
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get(url)
    print("🔄 Loading Meesho product page...")
    time.sleep(5)

    # Debug: Print a snippet of the page source to verify content
    print("DEBUG: Meesho page source snippet (first 1000 chars):")
    print(driver.page_source[:1000])

    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
    wait = WebDriverWait(driver, 20)

    title = None
    title_xpaths = [
        "//h1",
        "//h2",
        "//div[contains(@class, 'title')]"
    ]
    for xp in title_xpaths:
        try:
            title_element = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
            title = title_element.text.strip()
            if title:
                print(f"✅ Meesho Title found using XPath: {xp}")
                break
        except Exception as e:
            print(f"⚠️ Meesho Title not found with XPath {xp}: {e}")
    if not title:
        title = "Meesho Title not found"

    price = None
    price_xpaths = [
        "//h4[contains(text(),'₹')]",
        "//span[contains(text(),'₹')]",
        "//div[contains(@class, 'pdp-price')]"
    ]
    for xp in price_xpaths:
        try:
            price_element = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
            price_text = price_element.text.strip()
            if "₹" in price_text:
                price = price_text.replace("₹", "").replace(",", "").strip()
                print(f"✅ Meesho Price found using XPath: {xp}")
                break
        except Exception as e:
            print(f"⚠️ Meesho Price not found with XPath {xp}: {e}")
    if not price:
        price = "Meesho Price not found"

    meesho_data = {"Title": title, "Price": price}
    driver.quit()
    return meesho_data

if __name__ == "__main__":
    # Replace with actual product URLs from Amazon and Meesho
    amazon_url = "https://www.amazon.in/dp/B0BDK62PDX"  # Example Amazon URL
    meesho_url = "https://www.meesho.com/sample-product-url"  # Replace with an actual Meesho URL

    print("Scraping Amazon data...")
    amazon_data = get_amazon_data(amazon_url)
    print("Amazon Data:", amazon_data)

    print("\nScraping Meesho data...")
    meesho_data = get_meesho_data(meesho_url)
    print("Meesho Data:", meesho_data)

    # Compare the prices and output the best rate
    valid_prices = {}
    try:
        amazon_price = float(amazon_data["Price"]) if amazon_data["Price"] != "Amazon Price not found" else None
    except Exception:
        amazon_price = None
    try:
        meesho_price = float(meesho_data["Price"]) if meesho_data["Price"] != "Meesho Price not found" else None
    except Exception:
        meesho_price = None

    if amazon_price is not None:
        valid_prices["Amazon"] = amazon_price
    if meesho_price is not None:
        valid_prices["Meesho"] = meesho_price

    if valid_prices:
        best_site = min(valid_prices, key=valid_prices.get)
        best_price = valid_prices[best_site]
        print("\n✅ Best deal: {} at ₹{}".format(best_site, best_price))
    else:
        print("\n❌ No valid price data available to compare!")