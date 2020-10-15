import os, json, base64, boto3

firehose = boto3.client('firehose')

print('Loading function')

def recToFirehose(streamRecord):
    ddbRecord = streamRecord['NewImage']
    toFirehose = {}

    # Transform the record a bit
    try:
        dateStr = ddbRecord['date']['S']
    except:
        dateStr = ' '
    try:
        cases = json.loads(ddbRecord['cases']['N'])
    except:
        cases = 0
    try:
        deaths = json.loads(ddbRecord['deaths']['N'])
    except:
        deaths = 0
    try:
        recovered = json.loads(ddbRecord['recovered']['N'])
    except:
        recovered = 0

    toFirehose["date"] = dateStr
    toFirehose["cases"] = cases
    toFirehose["deaths"] = deaths
    toFirehose["recovered"] = recovered
    jtoFirehose = json.dumps(toFirehose)
    response = firehose.put_record(
      DeliveryStreamName=os.environ['DeliveryStreamName'],
      Record= {
          'Data': jtoFirehose + '\n'
      }
    )
    print(response)

def lambda_handler(event, context):
    
    print('Received Event\n{}'.format(event))
    for record in event['Records']:
        if (record['eventName']) != 'REMOVE':
            recToFirehose(record['dynamodb'])
    return 'Successfully processed {} records.'.format(len(event['Records']))