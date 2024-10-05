import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract URLs with a prefix
def extract_urls_with_prefix(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a', class_='text-decoration-none')
    
    urls = []
    for tag in a_tags:
        href = tag.get('href')
        if href:
            urls.append(f'https://www.odoo.com{href}')
    return urls

# Function to extract contact details from a given URL
def extract_contact_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    address_tag = soup.find('address')
    if address_tag:
        address = address_tag.get_text(separator="\n", strip=True)
        return address
    return 'No details found'

# Function to handle pagination and scrape all pages
def scrape_all_pages(base_url, start_page, end_page, output_file):
    all_data = []
    for page_number in range(start_page, end_page + 1):
        url = f"{base_url}?page={page_number}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        
        urls = extract_urls_with_prefix(url)
        for url in urls:
            print(f"Processing URL: {url}")
            contact_details = extract_contact_details(url)
            all_data.append([url, contact_details])
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(all_data, columns=["URL", "Contact Details"])
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)

# Example usage
base_url = 'https://www.odoo.com/partners/country/united-states-224'  # Replace with the base URL of the website
start_page = 1  # Starting page number
end_page = 11  # Ending page number
output_file = 'output.xlsx'  # Output file name
scrape_all_pages(base_url, start_page, end_page, output_file)

print(f"Output saved to {output_file}")
