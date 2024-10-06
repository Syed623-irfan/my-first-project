import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_company_names(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        h5_tags = soup.find_all('h5')
        data = []
        for h5 in h5_tags:
            h5_classes = h5.get('class', [])
            if 'mt-4' in h5_classes and 'mb-2' in h5_classes and 'col-12' in h5_classes:
                continue  # Skip this h5 tag
            
            company_name = h5.get_text(strip=True).replace('Filters', '').strip()
            if company_name:  # Ensure company_name is not empty
                data.append(company_name)
        return data
    else:
        return []

def scrape_multiple_pages(base_url, start_page, end_page, output_file):
    all_data = []
    for i in range(start_page, end_page + 1):
        url = f"{base_url}/page/{i}"
        data = get_company_names(url)
        all_data.extend(data)
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(all_data, columns=["Company Name"])
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)

# Example usage
base_url = 'https://www.odoo.com/partners/country/united-states-224'  # Replace with the actual base URL of the website
start_page = 1  # Starting page number
end_page = 11  # Ending page number
output_file = 'output.xlsx'  # Output file name
scrape_multiple_pages(base_url, start_page, end_page, output_file)

print(f"Output saved to {output_file}")
