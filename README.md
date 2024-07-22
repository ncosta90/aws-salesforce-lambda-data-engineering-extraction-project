# AWS-SFDC-Lambda: Data engineering extraction project

## Overview

This project focuses on data extraction using the Salesforce REST API. It involves extracting information from the Salesforce Accounts table using an AWS Lambda function, which then stores the data in S3 buckets. This event serves as a trigger for another Lambda function responsible for data transformation. The second Lambda function imports the new data from the previous S3 bucket, transforms it, and stores it back into a different S3 bucket. The entire process is implemented using Python.
