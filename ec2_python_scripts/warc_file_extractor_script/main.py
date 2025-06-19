import csv
import os
from urllib.parse import urlparse
from warcio.archiveiterator import ArchiveIterator
from newspaper import Article
from bs4 import BeautifulSoup

# Load allowed domains from CSV
allowed_domains = set()
with open('domains.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        allowed_domains.add(row['domain'].strip())

output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

with open('../../large_files/test.gz', 'rb') as stream:
    count = 0
    for idx, record in enumerate(ArchiveIterator(stream)):
        if record.rec_type != 'response':
            continue
        url = record.rec_headers.get_header('WARC-Target-URI')
        if not url:
            continue
        domain = urlparse(url).netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        if domain not in allowed_domains:
            continue
        payload = record.content_stream().read()
        try:
            html = payload.decode('utf-8', errors='replace')
        except Exception as e:
            html = ''
        # Use newspaper3k to extract article
        article = Article(url)
        article.set_html(html)
        try:
            article.parse()
            title = article.title
            article_text = article.text
        except Exception as e:
            title = ''
            article_text = ''
        # Fallback: if article_text is empty or very short, use BeautifulSoup to get all visible text
        if not article_text or len(article_text.strip()) < 500:
            soup = BeautifulSoup(html, 'html.parser')
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            all_text = soup.get_text(separator=' ', strip=True)
            article_text = all_text
        # Save to .txt file
        safe_domain = domain.replace('.', '_')
        filename = f'{idx+1}_{safe_domain}.txt'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f'URL: {url}\nDomain: {domain}\nTitle: {title}\n\n{article_text}\n')
        count += 1
        print(f'Saved: {filepath}')