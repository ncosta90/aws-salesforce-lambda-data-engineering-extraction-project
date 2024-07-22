# AWS-SFDC-Lambda: Data engineering extraction project

## Overview

This project focuses on data extraction using the Salesforce REST API. It involves extracting information from the Salesforce Accounts table using an AWS Lambda function, which then stores the data in S3 buckets. This event serves as a trigger for another Lambda function responsible for data transformation. The second Lambda function imports the new data from the previous S3 bucket, transforms it, and stores it back into a different S3 bucket. The entire process is implemented using Python.

## Architecture



Implement Complete Data Pipeline Data Engineering Project using Salesforce REST API

Integrating with SFDC REST API and extracting Data
Deploying code on AWS Lambda for Data Extraction
Adding trigger to run the extraction automatically
Writing transformation function
Building automated trigger on transformation function
Store files on S3 properly
Building Analytics Tables on data files using Glue and Athena
