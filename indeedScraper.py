import os, time, random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

def get_page_source(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon")))
        return driver.page_source
    except:
        return None

def scrape_jobs(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    jobs = []
    for job_card in soup.select("div.job_seen_beacon"):
        jobs.append({
            'Title': job_card.find('h2', class_='jobTitle').get_text(strip=True) if job_card.find('h2') else "N/A",
            'Company': job_card.find('span', {'class': lambda x: x and 'companyName' in x}).get_text(strip=True) if job_card.find('span', {'class': lambda x: x and 'companyName' in x}) else "N/A",
            'Location': job_card.find('div', class_='companyLocation').get_text(strip=True) if job_card.find('div', class_='companyLocation') else "N/A",
            'Job URL': "https://in.indeed.com" + job_card.find('a', class_='jcs-JobTitle')['href'] if job_card.find('a', class_='jcs-JobTitle') else "N/A"
        })
    return jobs

def save_data(data, file_format):
    df = pd.DataFrame(data)
    os.makedirs('output', exist_ok=True)
    filename = f"output/indeed_jobs_{time.strftime('%Y%m%d_%H%M%S')}.{file_format if file_format != 'excel' else 'xlsx'}"
    getattr(df, f"to_{file_format}")(
        filename, index=False, encoding='utf-8' if file_format != 'excel' else None, engine="openpyxl" if file_format == "excel" else None
    )
    print(f"Saved to {filename}")

def main():
    search_query, location, num_pages = input("Enter job title: "), input("Enter location: "), int(input("Pages to scrape: "))
    base_url, all_jobs, driver = f'https://in.indeed.com/jobs?q={search_query}&l={location}', [], create_driver()
    
    if not driver: return
    for page in range(num_pages):
        url = f"{base_url}&start={page * 10}"
        if (page_source := get_page_source(url, driver)): 
            all_jobs.extend(scrape_jobs(page_source))
            time.sleep(random.uniform(3, 6))
    
    driver.quit()
    if all_jobs:
        save_data(all_jobs, input("Enter file format (csv, json, excel): ").strip().lower())

if __name__ == "__main__":
    main()