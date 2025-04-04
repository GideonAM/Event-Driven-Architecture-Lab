import json
import os
import boto3
import urllib.parse
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function that is triggered by S3 object creation events and publishes messages to SNS.
    
    Args:
        event: The event dict from S3
        context: Lambda context
        
    Returns:
        Dict containing status and message
    """
    # Get environment variables
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    environment = os.environ['ENVIRONMENT']
    
    # Initialize SNS client
    sns_client = boto3.client('sns')
    
    try:
        # Extract bucket and object information from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        object_size = event['Records'][0]['s3']['object']['size']
        event_time = event['Records'][0]['eventTime']
        
        # Format the message
        message = {
            'environment': environment,
            'event_type': 'Object Created',
            'bucket_name': bucket_name,
            'object_key': object_key,
            'object_size_bytes': object_size,
            'event_time': event_time,
            'notification_time': datetime.utcnow().isoformat()
        }
        
        # Subject line for the email
        subject = f"[{environment.upper()}] New object uploaded to {bucket_name}"
        
        # Publish message to SNS topic
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(message, indent=2),
            Subject=subject
        )
        
        print(f"Successfully published notification: {response['MessageId']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Notification sent successfully',
                'messageId': response['MessageId']
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error sending notification: {str(e)}'
            })
        }
