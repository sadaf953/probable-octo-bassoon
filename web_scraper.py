import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def scrape_website(url):
    """
    Scrape a website and extract key information
    
    Args:
        url (str): URL of the website to scrape
    
    Returns:
        dict: Extracted website information or None if scraping fails
    """
    try:
        # Send a GET request to the URL with a user agent to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract different types of information
        return {
            'Title': soup.title.string if soup.title else 'No title found',
            'Headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            'Links': [a.get('href') for a in soup.find_all('a', href=True)],
            'Paragraphs': [p.get_text(strip=True) for p in soup.find_all('p')]
        }
    except requests.RequestException as e:
        st.error(f"Error fetching the website: {e}")
        return None

def validate_url(url):
    """
    Validate the input URL using a regex pattern
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if URL is valid, False otherwise
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def main():
    """
    Main Streamlit application for web scraping
    """
    st.title('Web Scraping Explorer 🕸️')
    
    # URL Input
    url = st.text_input('Enter Website URL to Scrape', placeholder='https://example.com')
    
    if st.button('Scrape Website'):
        # Validate URL
        if not url:
            st.warning('Please enter a URL')
            return
        
        if not validate_url(url):
            st.error('Invalid URL. Please enter a valid http or https URL.')
            return
        
        # Show loading spinner
        with st.spinner('Scraping website...'):
            # Perform scraping
            results = scrape_website(url)
        
        # Display results
        if results:
            # Title section
            st.subheader('Website Title')
            st.write(results['Title'])
            
            # Headings section
            st.subheader('Headings')
            if results['Headings']:
                for heading in results['Headings']:
                    st.text(heading)
            else:
                st.write('No headings found')
            
            # Links section
            st.subheader('Links')
            if results['Links']:
                for link in results['Links'][:20]:  # Limit to first 20 links
                    st.text(link)
            else:
                st.write('No links found')
            
            # Paragraphs section
            st.subheader('Paragraphs')
            if results['Paragraphs']:
                for para in results['Paragraphs'][:10]:  # Limit to first 10 paragraphs
                    st.text(para)
            else:
                st.write('No paragraphs found')

# Run the Streamlit app if this script is executed directly
if __name__ == '__main__':
    main()
