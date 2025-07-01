import os
import json
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import numpy as np

# Load environment variables
OPENSEARCH_ENDPOINT = os.environ.get('OpenSearchDomain.DomainEndpoint')
MODEL_ID = os.environ.get('model_id', 'amazon.titan-embed-text-v1')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
INDEX_NAME = 'policy-articles'

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

# Function to get basic index info
def get_index_info(endpoint=OPENSEARCH_ENDPOINT, region=AWS_REGION, index_name=INDEX_NAME):
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise Exception('Unable to get AWS credentials')
    
    # Get index mapping
    mapping_url = f"https://{endpoint}/{index_name}/_mapping"
    request = AWSRequest(method='GET', url=mapping_url)
    request.headers['Host'] = endpoint
    SigV4Auth(credentials, 'es', region).add_auth(request)
    headers = dict(request.headers)
    mapping_resp = requests.get(mapping_url, headers=headers)
    
    # Get index settings
    settings_url = f"https://{endpoint}/{index_name}/_settings"
    request = AWSRequest(method='GET', url=settings_url)
    request.headers['Host'] = endpoint
    SigV4Auth(credentials, 'es', region).add_auth(request)
    headers = dict(request.headers)
    settings_resp = requests.get(settings_url, headers=headers)
    
    # Get a few sample documents
    sample_url = f"https://{endpoint}/{index_name}/_search"
    sample_query = {"size": 3, "query": {"match_all": {}}}
    data = json.dumps(sample_query)
    request = AWSRequest(method='POST', url=sample_url, data=data.encode('utf-8'))
    request.headers['Content-Type'] = 'application/json'
    request.headers['Host'] = endpoint
    SigV4Auth(credentials, 'es', region).add_auth(request)
    headers = dict(request.headers)
    sample_resp = requests.post(sample_url, data=data, headers=headers)
    
    return {
        "mapping": mapping_resp.json() if mapping_resp.ok else f"Error: {mapping_resp.text}",
        "settings": settings_resp.json() if settings_resp.ok else f"Error: {settings_resp.text}",
        "sample_docs": sample_resp.json() if sample_resp.ok else f"Error: {sample_resp.text}"
    }

# Function to sign and post to OpenSearch
def search_opensearch_by_embedding(embedding, endpoint=OPENSEARCH_ENDPOINT, region=AWS_REGION, index_name=INDEX_NAME, k=3):
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise Exception('Unable to get AWS credentials')
    url = f"https://{endpoint}/{index_name}/_search"
    
    # First check if documents actually have embeddings
    check_url = f"https://{endpoint}/{index_name}/_search"
    check_query = {
        "size": 1,
        "query": {"exists": {"field": "embedding"}},
        "_source": ["title", "embedding"]
    }
    data = json.dumps(check_query)
    request = AWSRequest(method='POST', url=check_url, data=data.encode('utf-8'))
    request.headers['Content-Type'] = 'application/json'
    request.headers['Host'] = endpoint
    SigV4Auth(credentials, 'es', region).add_auth(request)
    headers = dict(request.headers)
    check_resp = requests.post(check_url, data=data, headers=headers)
    
    if check_resp.ok:
        check_result = check_resp.json()
        embedding_docs = check_result['hits']['total']['value']
        print(f"Documents with embeddings: {embedding_docs}")
        if embedding_docs == 0:
            print("ERROR: No documents have embeddings! This explains why k-NN search returns 0 results.")
            return {"hits": {"hits": [], "total": {"value": 0, "relation": "eq"}}}
    else:
        print(f"Error checking for embeddings: {check_resp.text}")

    # Try different query approaches - using the exact syntax from the example
    queries_to_try = [
        # Try k-NN with exact syntax from OpenSearch docs
        {
            "name": "knn_standard",
            "endpoint": "_search", 
            "query": {
                "size": k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": embedding,
                            "k": k
                        }
                    }
                },
                "_source": ["title", "summary", "sentiment_label", "sentiment_score"]
            }
        }
    ]
    
    resp = None
    for query_config in queries_to_try:
        print(f"Trying {query_config['name']} query...")
        url_with_endpoint = f"https://{endpoint}/{index_name}/{query_config['endpoint']}"
        data = json.dumps(query_config['query'])
        request = AWSRequest(method='POST', url=url_with_endpoint, data=data.encode('utf-8'))
        request.headers['Content-Type'] = 'application/json'
        request.headers['Host'] = endpoint
        SigV4Auth(credentials, 'es', region).add_auth(request)
        headers = dict(request.headers)
        resp = requests.post(url_with_endpoint, data=data, headers=headers)
        
        if resp.ok:
            print(f"{query_config['name']} query succeeded!")
            break
        else:
            print(f"{query_config['name']} query failed: {resp.status_code} {resp.text}")
    
    if not resp or not resp.ok:
        raise Exception(f"All query approaches failed. Last error: {resp.status_code if resp else 'No response'} {resp.text if resp else 'Unknown error'}")
    
    return resp.json()

# Function to check and update k-NN settings
def check_and_update_knn_settings(endpoint=OPENSEARCH_ENDPOINT, region=AWS_REGION, index_name=INDEX_NAME):
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise Exception('Unable to get AWS credentials')
    
    # Try to update index settings to enable k-NN functionality
    settings_url = f"https://{endpoint}/{index_name}/_settings"
    
    # First, close the index (required for some setting changes)
    close_url = f"https://{endpoint}/{index_name}/_close"
    request = AWSRequest(method='POST', url=close_url)
    request.headers['Host'] = endpoint
    SigV4Auth(credentials, 'es', region).add_auth(request)
    headers = dict(request.headers)
    close_resp = requests.post(close_url, headers=headers)
    
    if close_resp.ok:
        print("Index closed successfully")
        
        # Update settings to enable k-NN
        knn_settings = {
            "settings": {
                "index.knn": True,
            }
        }
        
        data = json.dumps(knn_settings)
        request = AWSRequest(method='PUT', url=settings_url, data=data.encode('utf-8'))
        request.headers['Content-Type'] = 'application/json'
        request.headers['Host'] = endpoint
        SigV4Auth(credentials, 'es', region).add_auth(request)
        headers = dict(request.headers)
        settings_resp = requests.put(settings_url, data=data, headers=headers)
        
        # Reopen the index
        open_url = f"https://{endpoint}/{index_name}/_open"
        request = AWSRequest(method='POST', url=open_url)
        request.headers['Host'] = endpoint
        SigV4Auth(credentials, 'es', region).add_auth(request)
        headers = dict(request.headers)
        open_resp = requests.post(open_url, headers=headers)
        
        if open_resp.ok:
            print("Index reopened successfully")
            if settings_resp.ok:
                print("k-NN settings updated successfully!")
                return True
            else:
                print(f"Failed to update k-NN settings: {settings_resp.text}")
                return False
        else:
            print(f"Failed to reopen index: {open_resp.text}")
            return False
    else:
        print(f"Failed to close index: {close_resp.text}")
        return False

if __name__ == "__main__":
    test_query = input("Enter your test query: ")
    embedding = get_bedrock_embedding(test_query)
    print("Embedding generated. Querying OpenSearch...")
    print(f"Embedding dimensions: {len(embedding) if embedding else 'None'}")
    
    # Increase k to ensure enough results for both sentiments
    results = search_opensearch_by_embedding(embedding, k=20)
    print(f"Full OpenSearch response: {json.dumps(results, indent=2)}")
    
    hits = results['hits']['hits']
    total_hits = results['hits']['total']
    print(f"Total hits found: {total_hits}")
    print(f"Returned hits: {len(hits)}")
    
    # If no hits, let's check the index info
    if len(hits) == 0:
        print("\nNo hits found. Checking index info...")
        try:
            index_info = get_index_info()
            print(f"Index mapping: {json.dumps(index_info['mapping'], indent=2)}")
            print(f"Index settings: {json.dumps(index_info['settings'], indent=2)}")
            
            # Check if k-NN is enabled in settings
            settings = index_info['settings']
            if isinstance(settings, dict):
                index_settings = settings.get(INDEX_NAME, {}).get('settings', {}).get('index', {})
                knn_enabled = index_settings.get('knn', False)
                print(f"\nk-NN enabled in index: {knn_enabled}")
                
                if not knn_enabled:
                    print("k-NN is not enabled! This explains why k-NN search returns 0 results.")
                    print("Attempting to enable k-NN settings...")
                    
                    if check_and_update_knn_settings():
                        print("k-NN settings updated! Retrying search...")
                        # Retry the search with updated settings
                        results = search_opensearch_by_embedding(embedding, k=20)
                        hits = results['hits']['hits']
                        total_hits = results['hits']['total']
                        print(f"After k-NN update - Total hits found: {total_hits}")
                        print(f"After k-NN update - Returned hits: {len(hits)}")
            
            # Print first document info
            sample_docs = index_info['sample_docs']
            if isinstance(sample_docs, dict) and 'hits' in sample_docs and 'hits' in sample_docs['hits']:
                sample_hits = sample_docs['hits']['hits']
                if sample_hits:
                    first_doc = sample_hits[0]['_source']
                    print(f"\nFirst document info:")
                    print(f"Title: {first_doc.get('title', 'N/A')}")
                    print(f"Summary length: {len(first_doc.get('summary', '')) if first_doc.get('summary') else 'N/A'}")
                    print(f"Vector length: {len(first_doc.get('embedding', [])) if first_doc.get('embedding') else 'N/A'}")
                else:
                    print("\nNo documents found in the index")
            else:
                print(f"Sample documents response: {json.dumps(sample_docs, indent=2)}")
        except Exception as e:
            print(f"Error getting index info: {e}")
    
    # Separate by sentiment
    positives = [hit for hit in hits if hit['_source']['sentiment_label'] == 'POSITIVE'][:5]
    negatives = [hit for hit in hits if hit['_source']['sentiment_label'] == 'NEGATIVE'][:5]

    print("Top 5 Positive Sentiment Articles:")
    for hit in positives:
        source = hit['_source']
        print(f"Title: {source['title']}")
        print(f"Summary: {source['summary']}")
        print(f"Sentiment: {source['sentiment_label']} (score: {source['sentiment_score']})")
        print(f"Score: {hit['_score']}")
        print('-' * 40)

    print("\nTop 5 Negative Sentiment Articles:")
    for hit in negatives:
        source = hit['_source']
        print(f"Title: {source['title']}")
        print(f"Summary: {source['summary']}")
        print(f"Sentiment: {source['sentiment_label']} (score: {source['sentiment_score']})")
        print(f"Score: {hit['_score']}")
        print('-' * 40)
