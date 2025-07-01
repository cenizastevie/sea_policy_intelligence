import os
import json
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

OPENSEARCH_ENDPOINT = os.environ.get('OpenSearchDomain.DomainEndpoint')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
INDEX_NAME = 'policy-articles'
EMBEDDING_DIM = 1536  # Change this if your embedding size is different

mapping = {
    "mappings": {
        "properties": {
            "embedding": {
                "type": "knn_vector",
                "dimension": EMBEDDING_DIM
            },
            "title": {"type": "text"},
            "summary": {"type": "text"},
            "sentiment_label": {"type": "keyword"},
            "sentiment_score": {"type": "float"}
        }
    }
}

def create_index_with_mapping():
    session = boto3.Session()
    credentials = session.get_credentials()
    url = f"https://{OPENSEARCH_ENDPOINT}/{INDEX_NAME}"
    data = json.dumps(mapping)
    request = AWSRequest(method='PUT', url=url, data=data.encode('utf-8'))
    request.headers['Content-Type'] = 'application/json'
    request.headers['Host'] = OPENSEARCH_ENDPOINT
    SigV4Auth(credentials, 'es', AWS_REGION).add_auth(request)
    headers = dict(request.headers)
    resp = requests.put(url, data=data, headers=headers)
    print(f"Status: {resp.status_code}")
    print(resp.text)

if __name__ == "__main__":
    create_index_with_mapping()