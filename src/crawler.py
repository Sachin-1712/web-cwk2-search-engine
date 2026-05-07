import time
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Document:
    """A single quote record captured from the target website."""

    doc_id: int
    text: str
    author: str
    tags: List[str]
    url: str
    
    def to_dict(self):
        return asdict(self)

def fetch_page(url: str, retries: int = 3) -> Optional[str]:
    """Fetch one HTML page, retrying transient request failures before giving up."""

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to fetch {url} after {retries} attempts.")
                return None

def crawl_quotes(base_url: str = 'https://quotes.toscrape.com', max_pages: Optional[int] = None, politeness_delay: float = 6.0) -> List[Document]:
    """
    Crawl paginated quote pages into Document objects.

    The default delay is six seconds to satisfy the coursework politeness
    requirement for real crawls. Tests and demos can pass a smaller delay.
    """

    documents = []
    current_page = '/page/1/'
    doc_id_counter = 1
    seen_texts = set()

    pages_scraped = 0

    while current_page:
        if max_pages and pages_scraped >= max_pages:
            break
            
        full_url = base_url + current_page
        logger.info(f"Crawling {full_url}...")
        
        html = fetch_page(full_url)
        if not html:
            break
            
        # Parse the HTML and find all quote containers on the current page
        soup = BeautifulSoup(html, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        for quote_div in quotes:
            text = quote_div.find('span', class_='text').get_text(strip=True)
            # Avoid indexing duplicate quote text if a page repeats content.
            if text in seen_texts:
                continue
            seen_texts.add(text)
            
            author = quote_div.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]
            
            doc = Document(
                doc_id=doc_id_counter,
                text=text,
                author=author,
                tags=tags,
                url=full_url
            )
            documents.append(doc)
            doc_id_counter += 1
            
        pages_scraped += 1
            
        next_btn = soup.find('li', class_='next')
        if next_btn:
            # Extract the relative URL for the next page of quotes
            current_page = next_btn.find('a')['href']
            logger.info(f"Politeness delay: sleeping for {politeness_delay} seconds...")
            time.sleep(politeness_delay)
        else:
            current_page = None
            
    return documents
