# aws-salesforce-lambda-data-engineering-extraction-project
A data extraction project using Salesforce REST API. Extracts data from the Salesforce Accounts table with an AWS Lambda function, storing it in an S3 bucket. This triggers another Lambda function for data transformation, which then stores the transformed data in a different S3 bucket. Implemented in Python.
