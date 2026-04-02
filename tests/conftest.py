import pytest
from src.crawler import Document

@pytest.fixture
def sample_documents():
    return [
        Document(
            doc_id=1,
            text='“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”',
            author='Albert Einstein',
            tags=['change', 'deep-thoughts', 'thinking', 'world'],
            url='http://quotes.toscrape.com/page/1/'
        ),
        Document(
            doc_id=2,
            text='“It is our choices, Harry, that show what we truly are, far more than our abilities.”',
            author='J.K. Rowling',
            tags=['abilities', 'choices'],
            url='http://quotes.toscrape.com/page/1/'
        ),
        Document(
            doc_id=3,
            text='“To be or not to be, that is the question.”',
            author='William Shakespeare',
            tags=['existential'],
            url='http://quotes.toscrape.com/page/2/'
        )
    ]
