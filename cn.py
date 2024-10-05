import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_h5_and_a_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        h5_tags = soup.find_all('h5')
        data = []
        for h5 in h5_tags:
            company_name = h5.get_text(strip=True).replace('Filters', '').strip()
            if company_name:  # Ensure company_name is not empty
                a_tag = h5.find_next_sibling('a', class_='badge mt-3 text-bg-secondary')
                industry_type = a_tag.get_text(strip=True) if a_tag else 'No industry found'
                data.append([company_name, industry_type])
        return data
    else:
        return []

def scrape_multiple_pages(base_url, start_page, end_page, output_file):
    all_data = []
    for i in range(start_page, end_page + 1):
        url = f"{base_url}/page/{i}"
        data = get_h5_and_a_text(url)
        all_data.extend(data)
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(all_data, columns=["Company Name", "Industry Type"])
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)

# Example usage
base_url = 'https://www.odoo.com/partners/country/canada-36'  # Replace with the actual base URL of the website
start_page = 1  # Starting page number
end_page = 5  # Ending page number
output_file = 'output.xlsx'  # Output file name
scrape_multiple_pages(base_url, start_page, end_page, output_file)

print(f"Output saved to {output_file}")
