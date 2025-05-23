from selectorlib import Extractor
import requests 
import json 
import os
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    data = e.extract(r.text)
    if data and 'products' in data:
        for product in data['products']:
            product['sponsored'] = product.get('sponsored') == 'Sponsored'
    return data

# Function to get search results from a URL
def get_search_results(url=None):
    """
    Scrapes Amazon search results from a specific URL or from search_results_urls.txt
    
    Args:
        url (str, optional): Amazon search URL. If None, reads from search_results_urls.txt
        
    Returns:
        list: List of product dictionaries from search results
    """
    if url is None:
        # Read the URL from file if not provided
        with open("search_results_urls.txt", 'r') as urlfile:
            url = urlfile.read().strip()
    
    # Scrape the URL
    data = scrape(url)
    
    products = []
    if data and 'products' in data:
        for product in data['products']:
            product['sponsored'] = product.get('sponsored') == 'Sponsored'
            product['search_url'] = url
            products.append(product)
    
    return products

# This code runs when the script is executed directly
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # product_data = []
    with open("search_results_urls.txt",'r') as urllist, open(os.path.join(output_dir, 'search_results_output.jsonl'),'w') as outfile:
        for url in urllist.read().splitlines():
            products = get_search_results(url)
            for product in products:
                print("Saving Product: %s"%product['title'])
                json.dump(product,outfile)
                outfile.write("\n")
                # sleep(5)
