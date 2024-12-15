from selenium.webdriver import Remote, ChromeOptions
# import selenium.webdriver as webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

load_dotenv()


# SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
SBR_WEBDRIVER='https://brd-customer-hl_65313b6b-zone-ai_scraper:d983lrrvzyj3@brd.superproxy.io:9515'
def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html
        



def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


# def search_and_collect_urls(course, country, limit=30):
#     print(f"masters in Artififical Intelligence in Australia")
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     options.add_argument('window-size=1920x1080')
#     driver = webdriver.Chrome(options=options)
#     search_query = f"masters in Artififical Intelligence in Australia"
#     driver.get("https://www.google.com")
#     search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
#     search_box.send_keys(search_query)
#     search_box.send_keys(Keys.RETURN)
#     try:
#         links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g > div > div > a")))
#         urls = [link.get_attribute("href") for link in links[:limit]]
#     except TimeoutException:
#         print("Timed out waiting for page to load")
#         urls = []
#     driver.quit()

#     with open('urls.txt', 'w') as f:
#         for url in urls:
#             f.write(f"{url}\n")

#     print(f"Collected {len(urls)} URLs and saved to urls.txt")
#     return urls