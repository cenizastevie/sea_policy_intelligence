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
