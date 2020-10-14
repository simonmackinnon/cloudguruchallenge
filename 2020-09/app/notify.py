import boto3
import os

def notify(subject, message):
    client = boto3.client('sns')
    
    topic = os.environ['SNS_TOPIC'] if os.environ['SNS_TOPIC'] else 'arn:aws:sns:ap-southeast-2:955966247963:SNSTopic-core-infrastructure-covid-app'
    
    response = client.publish(
        TopicArn=topic,
        Message=message,
        Subject=subject,
    )
    
    return(response)