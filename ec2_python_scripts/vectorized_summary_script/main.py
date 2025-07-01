import os
import pandas as pd
import boto3
import json
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from urllib.parse import urljoin
import hashlib

# Load environment variables
ARTICLES_VECTOR_BUCKET = os.environ.get('ArticlesVectorBucket', 'sea-articles-vector')
OPENSEARCH_ENDPOINT = os.environ.get('OpenSearchDomain.DomainEndpoint')
MODEL_ID = os.environ.get('model_id', 'amazon.titan-embed-text-v1')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# Function to get embedding from Bedrock

def get_bedrock_embedding(text, model_id=MODEL_ID):
    bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
    body = json.dumps({"inputText": text})
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

# Function to sign and post to OpenSearch

def post_to_opensearch(doc, index_name, endpoint=OPENSEARCH_ENDPOINT, region=AWS_REGION):
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise Exception('Unable to get AWS credentials')
    doc_id = hashlib.md5(doc['summary'].encode()).hexdigest()[:16]
    url = f"https://{endpoint}/{index_name}/_doc/{doc_id}"
    data = json.dumps(doc)
    request = AWSRequest(method='PUT', url=url, data=data.encode('utf-8'))
    request.headers['Content-Type'] = 'application/json'
    request.headers['Host'] = endpoint
    SigV4Auth(credentials, 'es', region).add_auth(request)
    headers = dict(request.headers)
    resp = requests.put(url, data=data, headers=headers)
    if not resp.ok:
        raise Exception(f"OpenSearch error: {resp.status_code} {resp.text}")
    return resp.json()

# Example: Load your DataFrame (replace with your actual loading logic)
results_df = pd.read_csv('summarized_sentiment_results.csv')
# ...existing code...

# For demonstration, assume results_df is already defined
# Iterate and post to OpenSearch
index_name = 'policy-articles'
for _, row in results_df.iterrows():
    summary = row['summary']
    embedding = get_bedrock_embedding(summary)
    doc = {
        'title': row['title'],
        'summary': summary,
        'sentiment_label': row['sentiment_label'],
        'sentiment_score': row['sentiment_score'],
        'embedding': embedding
    }
    result = post_to_opensearch(doc, index_name)
    print(f"Posted doc: {doc['title']} | OpenSearch result: {result}")
# ...existing code...