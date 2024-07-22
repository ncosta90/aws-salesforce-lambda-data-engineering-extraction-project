import json
import os
import boto3
import requests
from datetime import datetime

def lambda_handler(event, context):
    # Salesforce Credentials
    security_token = os.environ.get('security_token')
    sfdc_password = os.environ.get('sfdc_password')
    username = os.environ.get('username')
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    # Salesforce Authentication
    auth_url = 'https://login.salesforce.com/services/oauth2/token'
    auth_payload = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': sfdc_password + security_token
    }

    auth_response = requests.post(auth_url, data=auth_payload)
    auth_data = auth_response.json()
    access_token = auth_data['access_token']
    instance_url = auth_data['instance_url']

    # Headers for API requests
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Account table description
    describe_url = f'{instance_url}/services/data/v52.0/sobjects/Account/describe'
    describe_response = requests.get(describe_url, headers=headers)
    sfdc_account_table = describe_response.json()

    # SOQL
    sfdc_accounts_col_list = ['Id', 'Name', 'CreatedDate', 'Owner_Region__c', 'NumberOfEmployees']
    sfdc_accounts_col_string = ', '.join(sfdc_accounts_col_list)
    sfdc_accounts_col_query = f"SELECT {sfdc_accounts_col_string} FROM Account WHERE (NumberOfEmployees != NULL AND Owner_Region__c != NULL)"

    query_url = f'{instance_url}/services/data/v52.0/query?q={sfdc_accounts_col_query}'
    query_response = requests.get(query_url, headers=headers)
    sfdc_accounts_data = query_response.json()
    
    # Upload to S3
    client = boto3.client('s3')
    filename = "sfdc_accounts_data_raw_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".json"

    client.put_object(
        Bucket="salesforce-etl-accounts-project-nico",
        Key="raw_data/to_process/" + filename,
        Body=json.dumps(sfdc_accounts_data)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully fetched and uploaded to S3')
    }