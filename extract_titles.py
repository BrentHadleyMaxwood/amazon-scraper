import json
import os

def extract_unsponsored_titles(input_file='output/search_results_output.jsonl', output_file='output/titles_output.txt'):
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    titles = []
    with open(input_file, 'r') as jsonl_file:
        for line in jsonl_file:
            product = json.loads(line)
            if 'title' in product and product['title'] and not product['sponsored']:
                titles.append(product['title'])
    
    # Write titles to file
    with open(output_file, 'w', encoding='utf-8') as txt_file:
        for title in titles:
            txt_file.write(title + '\n')
    
    print(f"Successfully extracted {len(titles)} unsponsored titles to {output_file}")

def extract_titles_from_data(products):
    """
    Extract unsponsored titles from a list of product dictionaries
    
    Args:
        products (list): List of product dictionaries
        
    Returns:
        list: List of unsponsored product titles
    """
    titles = []
    for product in products:
        if 'title' in product and product['title'] and not product['sponsored']:
            titles.append(product['title'])
    
    return titles

if __name__ == "__main__":
    extract_unsponsored_titles()
