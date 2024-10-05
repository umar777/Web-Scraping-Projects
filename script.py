from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import time

GOOGLE_MAPS_API_KEY = ""

# Path to your ChromeDriver
CHROMEDRIVER_PATH = 'C:/Users/emira/OneDrive/Documents/Python Scripts/chromedriver/chromedriver.exe'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("disable-infobars")
#chrome_options.add_argument("--headless")  # Run in headless mode

# Initialize the WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def search_google(query):
    driver.get('https://www.google.co.uk/')
    
    try:
        # Wait for the consent screen and accept it if found
        try:
            wait = WebDriverWait(driver, 3)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Accept all']"))).click()
            print("Accepted Google consent screen.")
        except:
            print("No consent screen to accept.")

        # Pause to allow dynamic content to load fully
        time.sleep(2)  

        # Wait for the search box to be present and interactable
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'q'))
        )
        search_box.send_keys(query)
        search_box.submit()

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )
    except Exception as e:
        print(f"Error interacting with Google: {e}")
        driver.quit()
        return None

    return driver.page_source

# def extract_info(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     results = []

#     for g in soup.find_all('div', class_='g'):
#         title = g.find('h3')
#         if title:
#             title = title.get_text()
        
#         link = g.find('a', href=True)
#         if link:
#             link = link['href']
        
#         snippet = g.find('span', class_='aCOpRe')
#         if snippet:
#             snippet = snippet.get_text()
        
#         results.append({
#             'title': title,
#             'link': link,
#             'snippet': snippet
#         })
    
#     return results

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for g in soup.find_all('div', class_='rllt__details'):
        name = g.find('span', class_='OSrXXb')
        if name:
            name = name.get_text()

        # Extract address and phone number
        address_phone_div = g.find('div', text=lambda x: x and '·' in x)
        if address_phone_div:
            address_phone_text = address_phone_div.get_text()
            address, phone = map(str.strip, address_phone_text.split('·'))
        else:
            address, phone = None, None
        
        # Append the result
        results.append({
            'name': name,
            'address': address,
            'phone': phone
        })

    return results

def main():
    query = 'fragrances birmingham'
    html = search_google(query)
    
    if html:
        results = extract_info(html)
        for result in results:
            print(f"name: {result['name']}")
            print(f"address: {result['address']}")
            print(f"phone: {result['phone']}")
            print("-----")
    
    driver.quit()

if __name__ == '__main__':
    main()
