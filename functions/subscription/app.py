import json
import boto3
import cfnresponse
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Custom resource handler for managing SNS email subscriptions
    
    Args:
        event: CloudFormation custom resource event
        context: Lambda context
        
    Returns:
        CloudFormation custom resource response
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Initialize the SNS client
    sns_client = boto3.client('sns')
    
    # Get the request type
    request_type = event['RequestType']
    
    # Get properties from the event
    properties = event['ResourceProperties']
    topic_arn = properties.get('TopicArn')
    email_addresses = properties.get('EmailAddresses', [])
    
    # If received as a string, convert to list
    if isinstance(email_addresses, str):
        if email_addresses:
            email_addresses = [addr.strip() for addr in email_addresses.split(',')]
        else:
            email_addresses = []
    
    try:
        if request_type == 'Create' or request_type == 'Update':
            subscription_arns = []
            
            # Subscribe all email addresses
            for email in email_addresses:
                if email:  # Skip empty strings
                    logger.info(f"Subscribing {email} to {topic_arn}")
                    response = sns_client.subscribe(
                        TopicArn=topic_arn,
                        Protocol='email',
                        Endpoint=email
                    )
                    subscription_arns.append(response['SubscriptionArn'])
            
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                'SubscriptionArns': subscription_arns
            })
        
        elif request_type == 'Delete':
            # For deletion, we'll list all subscriptions and unsubscribe them
            paginator = sns_client.get_paginator('list_subscriptions_by_topic')
            for page in paginator.paginate(TopicArn=topic_arn):
                for subscription in page['Subscriptions']:
                    if subscription['Protocol'] == 'email':
                        logger.info(f"Unsubscribing {subscription['Endpoint']} from {topic_arn}")
                        # Note: SNS email subscriptions can't be deleted programmatically 
                        # if they're pending confirmation
                        if subscription['SubscriptionArn'] != 'PendingConfirmation':
                            sns_client.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
            
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                'Message': 'Deleted subscriptions'
            })
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {
            'Error': str(e)
        })
