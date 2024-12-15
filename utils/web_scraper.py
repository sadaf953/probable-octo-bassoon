import streamlit as st
from utils.web_tools import scrape_website, extract_text_content, validate_url

def main():
    st.title('Web Scraping Explorer 🕸️')
    url = st.text_input('Enter Website URL to Scrape', placeholder='https://example.com')

    if st.button('Scrape Website'):
        if not url:
            st.warning('Please enter a URL')
            return
        if not validate_url(url):
            st.error('Invalid URL.')
            return
        with st.spinner('Scraping website...'):
            try:
                soup = scrape_website(url)
                if soup:
                    text_content = extract_text_content(soup)
                    st.text_area("Extracted Content", text_content, height=500)  # Display extracted text
                else:
                    st.error("Website scraping failed.")
            except ValueError as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()