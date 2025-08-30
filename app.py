import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def setup_driver():
    options = Options()
    # Uncomment for headless mode after debugging
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

def get_amazon_data(url):
    driver = setup_driver()
    driver.get(url)
    print("🔄 Loading Amazon product page...")
    time.sleep(5)
    wait = WebDriverWait(driver, 20)

    title, price = "Amazon Title not found", "Amazon Price not found"
    try:
        title_element = wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
        title = title_element.text.strip()
    except Exception:
        pass
    
    try:
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'a-price-whole')]")))
        price = price_element.text.strip().replace(",", "")
    except Exception:
        pass
    
    driver.quit()
    return {"Title": title, "Price": price}

def get_meesho_data(url):
    driver = setup_driver()
    driver.get(url)
    print("🔄 Loading Meesho product page...")
    time.sleep(5)
    wait = WebDriverWait(driver, 20)

    title, price = "Meesho Title not found", "Meesho Price not found"
    try:
        title_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
        title = title_element.text.strip()
    except Exception:
        pass
    
    try:
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'₹')]")))
        price = price_element.text.strip().replace("₹", "").replace(",", "")
    except Exception:
        pass
    
    driver.quit()
    return {"Title": title, "Price": price}

def get_flipkart_data(url):
    driver = setup_driver()
    driver.get(url)
    print("🔄 Loading Flipkart product page...")
    time.sleep(5)
    wait = WebDriverWait(driver, 20)

    title, price = "Flipkart Title not found", "Flipkart Price not found"
    try:
        title_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='B_NuCI']")))
        title = title_element.text.strip()
    except Exception:
        pass
    
    try:
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_30jeq3 _16Jk6d')]")))
        price = price_element.text.strip().replace("₹", "").replace(",", "")
    except Exception:
        pass
    
    driver.quit()
    return {"Title": title, "Price": price}

if __name__ == "__main__":
    amazon_url = "https://www.amazon.in/dp/B0BDK62PDX"
    meesho_url = "https://www.meesho.com/sample-product-url"
    flipkart_url = "https://www.flipkart.com/sample-product-url"

    print("Scraping Amazon data...")
    amazon_data = get_amazon_data(amazon_url)
    print("Amazon Data:", amazon_data)

    print("\nScraping Meesho data...")
    meesho_data = get_meesho_data(meesho_url)
    print("Meesho Data:", meesho_data)
    
    print("\nScraping Flipkart data...")
    flipkart_data = get_flipkart_data(flipkart_url)
    print("Flipkart Data:", flipkart_data)
    
    valid_prices = {}
    for site, data in {"Amazon": amazon_data, "Meesho": meesho_data, "Flipkart": flipkart_data}.items():
        try:
            price = float(data["Price"]) if data["Price"] != f"{site} Price not found" else None
            if price is not None:
                valid_prices[site] = price
        except Exception:
            pass
    
    if valid_prices:
        best_site = min(valid_prices, key=valid_prices.get)
        best_price = valid_prices[best_site]
        print(f"\n✅ Best deal: {best_site} at ₹{best_price}")
    else:
        print("\n❌ No valid price data available to compare!")
