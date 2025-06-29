# Deploying the S3 Bucket (sea-news-articles) with CloudFormation

## Prerequisites
- AWS CLI installed and configured with appropriate permissions
- This template file saved locally (e.g., common-crawl-ingestion.yaml)

## Deployment Steps

1. Validate the template (optional but recommended):
   ```cmd
   aws cloudformation validate-template --template-body file://cloudformation/common-crawl-ingestion.yaml
   ```
2. Create the stack (replace <your-stack-name> with your desired stack name):
   ```cmd
   aws cloudformation create-stack --stack-name common-crawl-ingestion --template-body file://cloudformation/common-crawl-ingestion.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```
3. Wait for the stack to finish creating:
   ```cmd
   aws cloudformation describe-stacks --stack-name <your-stack-name>
   ```
4. (Optional) To update the stack in the future:
   ```cmd
   aws cloudformation update-stack --stack-name common-crawl-ingestion --template-body file://cloudformation/common-crawl-ingestion.yaml
   ```
5. (Optional) To delete the stack and all resources:
   ```cmd
   aws cloudformation delete-stack --stack-name <your-stack-name>
   ```

# CloudFormation Stack Deployment Instructions

## Prerequisites
- AWS CLI installed and configured with appropriate credentials
- AWS account with permissions to create IAM roles, S3 buckets, Glue databases, and Athena workgroups

## Deploy the Stack

1. **Navigate to the project directory:**
   ```cmd
   cd c:\Users\Steven\Desktop\Projects\sea_policy_intelligence
   ```

2. **Deploy the CloudFormation stack (first time):**
   ```cmd
   aws cloudformation create-stack --stack-name sea-policy-intelligence --template-body file://cloudformation/athena-common-crawl.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

3. **Update existing CloudFormation stack:**
   ```cmd
   aws cloudformation update-stack --stack-name sea-policy-intelligence --template-body file://cloudformation/athena-common-crawl.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

4. **Alternative: Use deploy command (works for both create and update):**
   ```cmd
   aws cloudformation deploy --stack-name sea-policy-intelligence --template-file cloudformation/athena-common-crawl.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

5. **Monitor the stack creation/update:**
   ```cmd
   aws cloudformation describe-stacks --stack-name sea-policy-intelligence --region us-east-1
   ```

6. **Get stack outputs (after successful creation/update):**
   ```cmd
   aws cloudformation describe-stacks --stack-name sea-policy-intelligence --region us-east-1 --query "Stacks[0].Outputs"
   ```

## What Gets Created

The CloudFormation stack creates:

- **S3 Buckets:**
  - `sea-policy-intelligence-athena-query-results` - For Athena query results
  - `sea-policy-intelligence-sea-policy-data` - For processed policy data

- **IAM Role:**
  - `sea-policy-intelligence-athena-execution-role` - With permissions to access Common Crawl data and your S3 buckets

- **Glue Database:**
  - `sea_policy_intelligence` - For storing table schemas

- **Athena Workgroup:**
  - `common-crawl-workgroup` - Configured to output results to your S3 bucket

## Next Steps

1. **Create Common Crawl Table in Athena:**
   - Use the AWS Athena console or run the table creation SQL
   - Point to Common Crawl's public S3 bucket

2. **Run Policy News Query:**
   - Use the query in `athena_queries/common_crawl_policy_news.sql`
   - Update crawl names to latest 6 months

3. **Process Results:**
   - Query results will be automatically stored in your query results S3 bucket
   - Use additional Glue tables to structure the processed data

## Cleanup

To delete the stack and all resources:
```cmd
aws cloudformation delete-stack --stack-name sea-policy-intelligence --region us-east-1
```

**Note:** You may need to empty the S3 buckets before deletion if they contain objects.

## Deploying batch-processing-resources.yaml as sea-batch-ingestion

To deploy the batch-processing-resources.yaml CloudFormation stack as sea-batch-ingestion, use the AWS CLI:

```
aws cloudformation deploy --stack-name sea-batch-ingestion --template-file cloudformation/batch-processing-resources.yaml --capabilities CAPABILITY_NAMED_IAM
```

This will create or update the stack named sea-batch-ingestion using the provided template. Ensure your AWS CLI is configured with the correct credentials and region.

## Deploying bedrock-opensearch.yaml as sea-bedrock-opensearch

### Prerequisites
- AWS CLI installed and configured with appropriate credentials
- The `common-crawl-ingestion` stack must be deployed first (for ArticlesVectorBucket export)
- Bedrock access enabled in your AWS region (us-east-1, us-west-2, etc.)
- Enable Amazon Titan Embed Text v1 model in Bedrock console

### Required IAM Permissions
Your deployment user/role needs these permissions:
- `CloudFormationFullAccess` 
- `IAMFullAccess`
- `AWSLambdaFullAccess`
- `AmazonOpenSearchServiceFullAccess`
- Custom Bedrock policy (see below)

### Custom Bedrock Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}
```

### Deployment Steps

1. **Navigate to the project directory:**
   ```cmd
   cd c:\Users\Steven\Desktop\Projects\sea_policy_intelligence
   ```

2. **Validate the template (optional but recommended):**
   ```cmd
   aws cloudformation validate-template --template-body file://cloudformation/bedrock-opensearch.yaml
   ```

3. **Deploy the CloudFormation stack (first time):**
   ```cmd
   aws cloudformation create-stack --stack-name sea-bedrock-opensearch --template-body file://cloudformation/bedrock-opensearch.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

4. **Update existing CloudFormation stack:**
   ```cmd
   aws cloudformation update-stack --stack-name sea-bedrock-opensearch --template-body file://cloudformation/bedrock-opensearch.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

5. **Alternative: Use deploy command (works for both create and update):**
   ```cmd
   aws cloudformation deploy --stack-name sea-bedrock-opensearch --template-file cloudformation/bedrock-opensearch.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

6. **Monitor the stack creation/update:**
   ```cmd
   aws cloudformation describe-stacks --stack-name sea-bedrock-opensearch --region us-east-1
   ```

7. **Get stack outputs (after successful creation/update):**
   ```cmd
   aws cloudformation describe-stacks --stack-name sea-bedrock-opensearch --region us-east-1 --query "Stacks[0].Outputs"
   ```

### What Gets Created

The CloudFormation stack creates:

- **IAM Role:**
  - `sea-policy-intelligence-bedrock-lambda-role` - With permissions for Bedrock, OpenSearch, and S3

- **Lambda Function:**
  - `sea-policy-intelligence-bedrock-embeddings` - Generates embeddings and posts to OpenSearch
  - Runtime: Python 3.11, Memory: 1024MB, Timeout: 5 minutes

- **OpenSearch Domain:**
  - `sea-policy-intelligence-opensearch` - Single t3.small.search instance
  - 10GB gp3 storage, HTTPS enforced, encryption enabled
  - Takes 10-15 minutes to create

### Testing the Deployment

1. **Test the Lambda function with default test sentence:**
   ```cmd
   aws lambda invoke --function-name sea-policy-intelligence-bedrock-embeddings --payload "{}" response.json --region us-east-1
   ```

2. **Test with custom text:**
   ```cmd
   aws lambda invoke --function-name sea-policy-intelligence-bedrock-embeddings --payload "{\"text\":\"Custom policy text here\"}" response.json --region us-east-1
   ```

3. **View the response:**
   ```cmd
   type response.json
   ```

### Accessing OpenSearch

- **OpenSearch Endpoint:** Available in stack outputs
- **Dashboard URL:** `https://{domain-endpoint}/_dashboards/`
- **Default Index:** `policy-articles` (created automatically)

### Cost Estimation

- **OpenSearch t3.small.search:** ~$26/month
- **Lambda:** Pay per invocation (~$0.70/month for 1000 calls)
- **Bedrock Titan Embed:** $0.0001 per 1K tokens
- **Total:** ~$30-50/month for moderate usage

### Cleanup

To delete the stack and all resources:
```cmd
aws cloudformation delete-stack --stack-name sea-bedrock-opensearch --region us-east-1
```

**Note:** The OpenSearch domain deletion takes 10-15 minutes.
