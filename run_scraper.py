import os
import sys
import argparse
import subprocess
from searchresults import get_search_results
from extract_titles import extract_titles_from_data

def create_amazon_search_url(keyword):
    """Create an Amazon search URL from a keyword"""
    # Format the keyword for a URL by replacing spaces with '+'
    formatted_keyword = keyword.replace(' ', '+')
    return f"https://www.amazon.com/s?k={formatted_keyword}"

def get_ranked_titles(keyword, num_titles=10):
    """
    Scrape Amazon search results for a keyword and return top unsponsored titles with their rank.
    
    Args:
        keyword (str): Keyword to search on Amazon
        num_titles (int): Maximum number of titles to return
        
    Returns:
        str: Formatted text with titles and their ranks
    """
    # Create search URL
    search_url = create_amazon_search_url(keyword)
    
    # Get search results directly
    products = get_search_results(search_url)
    
    # Extract titles from the data
    titles = extract_titles_from_data(products)
    
    # Format the results as a ranked list
    result = f"Top {min(num_titles, len(titles))} unsponsored product titles for '{keyword}':\n\n"
    
    for i, title in enumerate(titles[:num_titles], 1):
        result += f"{i}. {title}\n"
    
    return result

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Amazon scraper with a keyword')
    parser.add_argument('keyword', help='Keyword to search Amazon for')
    parser.add_argument('--num-titles', type=int, default=10, 
                        help='Number of titles to return (default: 10)')
    parser.add_argument('--scrape-products', action='store_true', 
                        help='Also scrape individual product pages from search results')
    args = parser.parse_args()
    
    # Get the ranked titles
    ranked_titles = get_ranked_titles(args.keyword, args.num_titles)
    print(ranked_titles)
    
    # Optionally run amazon.py to scrape individual product pages
    if args.scrape_products:
        print("\nScraping individual product pages...")
        # Write the search URL to file for backward compatibility
        with open("search_results_urls.txt", 'w') as url_file:
            url_file.write(create_amazon_search_url(args.keyword))
        # Run the script
        subprocess.run([sys.executable, "amazon.py"])
    
    return ranked_titles

if __name__ == "__main__":
    main()
