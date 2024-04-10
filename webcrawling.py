import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to recursively crawl a webpage up to a specified depth and return extracted text
def crawl_webpage(url, max_depth, current_depth=0):
    if current_depth > max_depth:
        return []

    try:
        # Make an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract visible text content from the current page
        text_content = []
        for element in soup.find_all(string=True):
            if element.parent.name not in ['script', 'style']:
                text_content.append(element.strip())
        webpage_text = ' '.join(text_content)

        # Print or store the extracted text content
        print(f"Depth {current_depth}: {url}")
        # print(webpage_text[:200])  # Print a snippet of the extracted text

        # Find and crawl links to other pages (e.g., tabs or sections)
        links = [link['href'] for link in soup.find_all('a', href=True)]
        extracted_texts = [webpage_text]  # Start with the current page's text

        for link in links:
            absolute_link = urljoin(url, link)  # Convert relative URLs to absolute URLs
            extracted_texts += crawl_webpage(absolute_link, max_depth, current_depth + 1)

        return extracted_texts

    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")
        return []

if __name__ == "__main__":
    # Example URL to start crawling
    start_url = 'https://www.t-systems.com/de/de'
    extracted_texts = crawl_webpage(start_url, max_depth=1)  # Specify the maximum depth of crawling