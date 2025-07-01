# sea_policy_intelligence
This repository showcases "SEA Policy Intelligence," a personal project utilizing an AWS-powered data pipeline to extract and analyze information on government projects, initiatives, and their impacts across Southeast Asian countries, sourced from the vast Common Crawl web archive, all for the purpose of generating public policy insights.

**Important:**  
Before ingesting any data into OpenSearch, you must first run the index mapping script located at `ec2_python_scripts/opensearch_mapping_script/main.py`. This script sets up the required index and mapping for vector search in OpenSearch.