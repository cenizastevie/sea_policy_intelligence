import csv
import os
from urllib.parse import urlparse
from warcio.archiveiterator import ArchiveIterator
from newspaper import Article
from bs4 import BeautifulSoup
import re
import os
import boto3
from s3 import upload_bytes, get_input_file_stream, get_warc_file_stream

def sanitize_filename(url):
    parsed = urlparse(url)
    path = parsed.path + (('_' + parsed.query) if parsed.query else '')
    if not path or path == '/':
        path = 'root'
    safe_path = re.sub(r'[^a-zA-Z0-9]', '_', path)
    if safe_path[0] == '_':
        safe_path = safe_path[1:]
    if safe_path.endswith('_'):
        safe_path = safe_path[:-1]
    return f'{safe_path}.txt'

def process_warc_stream(stream):
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
        if not article_text or len(article_text.strip()) < 500:
            soup = BeautifulSoup(html, 'html.parser')
            for script in soup(['script', 'style']):
                script.decompose()
            all_text = soup.get_text(separator=' ', strip=True)
            article_text = all_text
        safe_domain = domain.replace('.', '_')
        filename = sanitize_filename(url)
        s3_key = f'{safe_domain}/{filename}'
        upload_bytes(
            f'URL: {url}\nDomain: {domain}\nTitle: {title}\n\n{article_text}\n'.encode('utf-8'),
            s3_key,
            url,
            title
        )

if __name__ == '__main__':
    batch_file_manifest = os.environ.get('BATCH_FILE_MANIFEST', 'batch_file_manifest_test.csv')
    batch_csv_stream = get_input_file_stream(batch_file_manifest)
    batch_csv_reader = csv.DictReader(batch_csv_stream.read().decode('utf-8').splitlines())
    warc_files = [row['wet_file_s3_path'].strip() for row in batch_csv_reader]

    allowed_domains = set()
    with open('domains.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            allowed_domains.add(row['domain'].strip())

    for warc_file in warc_files:
        print(f'Processing WARC file: {warc_file}')
        warc_stream = get_warc_file_stream(warc_file)
        process_warc_stream(warc_stream)
        print(f'Finished processing WARC file: {warc_file}')