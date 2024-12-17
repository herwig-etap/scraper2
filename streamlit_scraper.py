# File: streamlit_scraper.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data
def scrape_website(url, product_selector, name_selector, price_selector, image_selector):
    try:
        # Send HTTP request to the target URL
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"Failed to fetch the URL. Status code: {response.status_code}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find product containers
        products = soup.select(product_selector)  # General product container
        scraped_data = []

        # Extract product details
        for product in products:
            name = product.select_one(name_selector).get_text(strip=True) if product.select_one(name_selector) else "N/A"
            price = product.select_one(price_selector).get_text(strip=True) if product.select_one(price_selector) else "N/A"
            image = product.select_one(image_selector)['src'] if product.select_one(image_selector) else "N/A"

            scraped_data.append({
                "Name": name,
                "Price": price,
                "Image URL": image
            })

        return scraped_data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Streamlit UI
def main():
    st.title("Web Scraper Tool with Streamlit")
    st.write("Enter the URL and selectors to scrape product data.")

    # User inputs
    url = st.text_input("Enter the website URL", "https://example.com/products")
    product_selector = st.text_input("Product Container CSS Selector", "div.product-card")
    name_selector = st.text_input("Product Name CSS Selector", "h2.product-title")
    price_selector = st.text_input("Price CSS Selector", "span.product-price")
    image_selector = st.text_input("Image CSS Selector", "img.product-image")

    # Scrape button
    if st.button("Scrape"):
        with st.spinner("Scraping in progress..."):
            data = scrape_website(url, product_selector, name_selector, price_selector, image_selector)

        if data:
            # Display scraped data
            st.success("Scraping completed successfully!")
            df = pd.DataFrame(data)
            st.dataframe(df)

            # Download options
            st.download_button("Download CSV", df.to_csv(index=False), "scraped_data.csv", "text/csv")
            st.download_button("Download JSON", df.to_json(orient="records"), "scraped_data.json", "application/json")
        else:
            st.warning("No data scraped. Check the selectors or URL.")

if __name__ == "__main__":
    main()
