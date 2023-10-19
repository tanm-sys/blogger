import requests
import random
import concurrent.futures
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
import time
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = input("URL --> ")
num_requests = int(input("Number of requests per thread --> "))
num_threads = int(input("Number of threads --> "))
max_clicks = 3  # Maximum number of clicks to simulate

ua = UserAgent()

def fetch_page(url, headers, timeout):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch page: {e}")
        return None

def get_valid_links(soup, base_url):
    valid_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http') and urlparse(href).netloc == urlparse(base_url).netloc:
            valid_links.append(href)
    return valid_links

def simulate_clicks(url, headers, timeout, remaining_clicks=max_clicks):
    if remaining_clicks > 0:
        page_content = fetch_page(url, headers, timeout)
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            valid_links = get_valid_links(soup, url)
            if valid_links:
                link_to_click = random.choice(valid_links)
                logging.info(f"Simulating click on {link_to_click}")
                simulate_clicks(link_to_click, headers, timeout, remaining_clicks - 1)

def run_threads(url, num_requests, num_threads, timeout):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_requests):
            headers = {'User-Agent': ua.random}
            simulate_clicks(url, headers, timeout)
            time.sleep(random.uniform(1, 5))  # Random sleep time between 1 to 5 seconds

if __name__ == '__main__':
    run_threads(url, num_requests, num_threads, timeout=5)
