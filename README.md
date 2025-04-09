# Event-Driven S3 Upload Notification System

A serverless application built with AWS SAM that sends email notifications when files are uploaded to an S3 bucket.

## Architecture

This project implements a simple event-driven architecture using:
- Amazon S3 for file storage
- AWS Lambda for event processing
- Amazon SNS for notifications

![event-driven-architecture-diagram](https://github.com/user-attachments/assets/399080f6-fc5e-4037-90f1-2e49f54e7e57)


When a file is uploaded to the S3 bucket, a Lambda function is triggered, which then publishes a message to an SNS topic. The topic sends an email notification to subscribed email addresses.

## Prerequisites

- AWS Account
- AWS CLI configured with appropriate credentials
- AWS SAM CLI
- Java 17
- Maven

## Project Structure

```
/
├── template.yaml         
├── samconfig.toml  
├── pom.xml           
└── src/
    └── main/
        └── java/
            └── com/
                └── redeemerlives/
                    └── EventDrivenArchitecture.java 
```

## Deployment

### Local Development

1. Build the project:
   ```
   sam build
   ```

2. Deploy to AWS:
   ```
   sam deploy --guided
   ```

### CI/CD with GitHub Actions

This project includes a GitHub Actions workflow to automate deployment to development and production environments based on branch:
- Push to `test` branch: Deploys to development environment
- Push to `main` branch: Deploys to production environment
