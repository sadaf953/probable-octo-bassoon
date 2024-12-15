from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


load_dotenv()

#Set webdriver in .env file
SCRAPING_BROWSER_URL = os.getenv("SCRAPING_BROWSER_URL")
if not SCRAPING_BROWSER_URL:
    raise ValueError("SCRAPING_BROWSER_URL environment variable not set.")

def scrape_website(website, timeout_seconds=10):
    """Scrapes a website using a scraping browser service.  Handles timeouts and errors."""
    print(f"Connecting to Scraping Browser: {SCRAPING_BROWSER_URL}")
    try:
        options = ChromeOptions()
        with Remote(command_executor=SCRAPING_BROWSER_URL, options=options) as driver:
            driver.get(website)
            # Explicit wait for the captcha to be solved, handle Timeouts
            try:
                WebDriverWait(driver, timeout_seconds).until(EC.presence_of_element_located((By.TAG_NAME,"body"))) #Check if body is loaded
                print("Page loaded. Captcha likely solved.")
            except TimeoutException:
                print(f"Timeout waiting for page to load after {timeout_seconds} seconds.")
                return "" # Return empty string if timeout


            html = driver.page_source
            return html

    except WebDriverException as e:
        print(f"Selenium WebDriver error: {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e}")
        return ""


def extract_body_content(html_content):
    """Extracts body content from HTML using Beautiful Soup."""
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    return str(body) if body else ""


def clean_body_content(body_content):
    """Cleans body content by removing scripts and styles, and extra whitespace."""
    soup = BeautifulSoup(body_content, "html.parser")
    for element in soup(["script", "style"]):
        element.extract()  #Removes these elements from the tree
    text = soup.get_text(separator="\n")
    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return cleaned_text


def split_dom_content(dom_content, max_length=6000):
    """Splits DOM content into chunks of specified max_length."""
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]