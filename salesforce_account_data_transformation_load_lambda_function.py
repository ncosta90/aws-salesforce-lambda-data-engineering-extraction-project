import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd

def account(data):
    account_list = []
    for row in data['records']:
        account_Id = row['Id']
        account_Name = row['Name']
        account_CreatedDate = row['CreatedDate']
        account_Owner_Region__c = row['Owner_Region__c']
        account_NumberOfEmployees = row['NumberOfEmployees']
        extracting_date = pd.Timestamp.now()
        account_element = {
            'account_id': account_Id,
            'name': account_Name,
            'creation_date': account_CreatedDate,
            'owner_region': account_Owner_Region__c,
            'total_employees': account_NumberOfEmployees,
            'extracting_date': extracting_date
        }
        account_list.append(account_element)
    return account_list
    
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "salesforce-etl-accounts-project-nico"
    Key = "raw_data/to_process/"

    sfdc_account_data = []
    sfdc_account_data_keys = []
    
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1] == "json":
            response = s3.get_object(Bucket = Bucket, Key = file_key)
            content = response['Body'].read().decode('utf-8')
            jsonObject = json.loads(content)
            sfdc_account_data.append(jsonObject)
            sfdc_account_data_keys.append(file_key)
            
    for data in sfdc_account_data:
        account_list = account(data)

        account_df = pd.DataFrame(account_list)
        account_df['creation_date'] = pd.to_datetime(account_df['creation_date']).dt.strftime('%Y-%m-%d')
        account_df['extracting_date'] = account_df['extracting_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        account_key = "transformed_data/account_data/account_data_transformed_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".csv"
        account_buffer=StringIO()
        account_df.to_csv(account_buffer, index=False)
        account_content = account_buffer.getvalue()
        account_buffer.close()
        s3.put_object(Bucket=Bucket, Key=account_key, Body=account_content)
        
    s3_resource = boto3.resource('s3')
    for key in sfdc_account_data_keys:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])    
        s3_resource.Object(Bucket, key).delete()