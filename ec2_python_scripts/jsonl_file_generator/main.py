import boto3
import json
import os
from io import BytesIO

def list_prefixes(bucket):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    prefixes = set()
    for page in paginator.paginate(Bucket=bucket, Delimiter='/'):
        for prefix in page.get('CommonPrefixes', []):
            prefixes.add(prefix['Prefix'].rstrip('/'))
    return list(prefixes)

def list_objects_with_prefix(bucket, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    objects = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix+'/'):
        for obj in page.get('Contents', []):
            objects.append(obj['Key'])
    return objects

def get_object_metadata_and_content(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    metadata = obj.get('Metadata', {})
    content = obj['Body'].read().decode('utf-8', errors='replace')
    return metadata, content

def write_jsonl_file(prefix, records):
    filename = f'{prefix}.jsonl'
    with open(filename, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    return filename

def upload_file_to_bucket(filename, bucket, key):
    s3 = boto3.client('s3')
    s3.upload_file(filename, bucket, key)

def main():
    source_bucket = 'sea-news-articles'
    dest_bucket = 'sea-articles-jsonl'
    prefixes = list_prefixes(source_bucket)
    for prefix in prefixes:
        print(f'Processing prefix: {prefix}')
        objects = list_objects_with_prefix(source_bucket, prefix)
        records = []
        for key in objects:
            metadata, content = get_object_metadata_and_content(source_bucket, key)
            record = {
                'url': metadata.get('url', ''),
                'title': metadata.get('title', ''),
                'language': metadata.get('language', ''),
                'domain': metadata.get('domain', ''),
                'warc_file': metadata.get('warc_file', ''),
                'scrape_date': metadata.get('scrape_date', ''),
                'content': content
            }
            records.append(record)
        jsonl_filename = write_jsonl_file(prefix, records)
        upload_file_to_bucket(jsonl_filename, dest_bucket, os.path.basename(jsonl_filename))
        print(f'Uploaded {jsonl_filename} to {dest_bucket}')
        os.remove(jsonl_filename)

if __name__ == '__main__':
    main()
