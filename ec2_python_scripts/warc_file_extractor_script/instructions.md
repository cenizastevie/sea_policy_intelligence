# Instructions: Build and Upload Docker Image to ECR for AWS Batch

## Prerequisites
- AWS CLI installed and configured
- Docker installed and running
- ECR repository created (e.g., sea-batch-task-repo)
- (Optional) Login to AWS Console and get your AWS Account ID and region

## 1. Authenticate Docker to your ECR registry
Replace <aws_account_id> and <region> with your values:

```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 211626350366.dkr.ecr.us-east-1.amazonaws.com
```

## 2. Build the Docker image
From the `ec2_python_scripts/warc_file_extractor_script` directory:

```
docker build -t sea-batch-task-repo .
```

## 3. Tag the image for ECR
```
docker tag sea-batch-task-repo:latest 211626350366.dkr.ecr.us-east-1.amazonaws.com/sea-batch-task-repo:latest
```

## 4. Push the image to ECR
```
docker push 211626350366.dkr.ecr.us-east-1.amazonaws.com/sea-batch-task-repo:latest
```

## 5. Use this image URI in your AWS Batch Job Definition

---

Replace `<aws_account_id>` and `<region>` with your actual AWS account ID and region.
