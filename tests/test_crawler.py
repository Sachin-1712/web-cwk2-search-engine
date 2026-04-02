import pytest
import requests
from src.crawler import crawl_quotes, fetch_page

def test_fetch_page_success(requests_mock):
    url = "http://example.com"
    requests_mock.get(url, text="<html>Success</html>")
    
    html = fetch_page(url)
    assert html == "<html>Success</html>"

def test_fetch_page_retry_failure(requests_mock, mocker):
    url = "http://example.com"
    # Always fail
    requests_mock.get(url, exc=requests.exceptions.ConnectionError)
    
    # Mock sleep so tests run fast
    mock_sleep = mocker.patch("src.crawler.time.sleep")
    
    html = fetch_page(url, retries=2)
    assert html is None
    assert mock_sleep.call_count == 1  # Called for the first failure before retry

def test_crawl_quotes(requests_mock, mocker):
    base_url = "http://quotes.toscrape.com"
    
    html_page_1 = """
    <html>
        <div class="quote">
            <span class="text">"Quote 1"</span>
            <small class="author">Author 1</small>
            <a class="tag">tag1</a>
        </div>
        <li class="next"><a href="/page/2/">Next</a></li>
    </html>
    """
    
    html_page_2 = """
    <html>
        <div class="quote">
            <span class="text">"Quote 2"</span>
            <small class="author">Author 2</small>
            <a class="tag">tag1</a>
            <a class="tag">tag2</a>
        </div>
        <!-- No next button -->
    </html>
    """
    
    requests_mock.get(f"{base_url}/page/1/", text=html_page_1)
    requests_mock.get(f"{base_url}/page/2/", text=html_page_2)
    
    # Speed up delay
    mocker.patch("src.crawler.time.sleep")
    
    docs = crawl_quotes(base_url, politeness_delay=0.1)
    
    assert len(docs) == 2
    assert docs[0].text == '"Quote 1"'
    assert docs[0].author == 'Author 1'
    assert docs[0].tags == ['tag1']
    assert docs[0].url == f"{base_url}/page/1/"
    
    assert docs[1].text == '"Quote 2"'
    assert docs[1].url == f"{base_url}/page/2/"

def test_crawl_duplicate_avoidance(requests_mock, mocker):
    base_url = "http://quotes.toscrape.com"
    
    html_page = """
    <html>
        <div class="quote">
            <span class="text">"Duplicate"</span>
            <small class="author">Author 1</small>
        </div>
        <div class="quote">
            <span class="text">"Duplicate"</span>
            <small class="author">Author 2</small>
        </div>
    </html>
    """
    requests_mock.get(f"{base_url}/page/1/", text=html_page)
    mocker.patch("src.crawler.time.sleep")
    
    docs = crawl_quotes(base_url)
    # The duplicate (identified by text) should be skipped
    assert len(docs) == 1
    assert docs[0].author == 'Author 1'
