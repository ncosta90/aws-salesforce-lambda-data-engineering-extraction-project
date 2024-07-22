# AWS-SFDC-Lambda: Data engineering extraction project

## Project Overview

This project focuses on data extraction using the Salesforce REST API. It involves extracting information from the Salesforce Accounts table using an AWS Lambda function + Cloud Watch, which then stores the data in S3 buckets. This event triggers another Lambda function responsible for data transformation. The second Lambda function imports the new data from the first S3 bucket, transforms it, and stores it back into a different S3 bucket.

Following this, AWS Glue Crawler and Data Catalog are used to automatically discover and catalog the new data, making it available for querying. Finally, Amazon Athena is used to analyze the transformed data directly from the S3 buckets using SQL queries.

## Architecture
![Architecture](https://github.com/ncosta90/aws-salesforce-lambda-data-engineering-extraction-project/blob/main/Architecture.jpeg)

## Salesforce Account Table

The Account table in Salesforce contains information about companies or organizations with which you do business. For this project, we are focusing only on the following fields:

Id: The unique identifier for each account.
Name: The name of the account (company or organization).
Creation Date: The date when the account was created.
Owner Region: The geographic region of the account owner.
Size/Number of Employees: The size of the account in terms of employee count.

We will update our customer table every 4 hours using AWS Lambda and CloudWatch to ensure the data remains current.

## AWS Services Used
1. **S3 (Simple Storage Service):** Scalable object storage for storing and retrieving any amount of data.
2. **AWS Lambda:** Serverless compute service that runs code in response to events.
3. **Cloud Watch:** Monitoring and observability service for tracking AWS resources and applications.
4. **AWS Glue Crawler:** Automatically discovers and catalogs data for analytics.
5. **Data Catalog:** Metadata repository for managing and searching data.
6. **Amazon Athena:** SQL-based query service for analyzing data in S3.
