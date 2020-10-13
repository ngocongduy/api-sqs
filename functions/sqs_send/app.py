import json
import boto3
from datetime import datetime
def lambda_handler(event, context):

    print(event)
    print(type(event))

    sys = event.get('Sys')
    info = event.get('Info')
    print(sys)
    print(type(sys))
    print(info)
    print(type(info))
    # Do something to validate input

    # Create SQS client
    sqs = boto3.client('sqs')
    queue = sqs.create_queue(QueueName="QueueForAPI.fifo",
        Attributes={"FifoQueue": "True"}

    )
    queue_url = queue.get('QueueUrl')

    queue_att = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ]
    )
    print(queue_att)
    dt = datetime.now()
    time_call = 'Time call: {}'.format(str(dt))
    dt_int = int(dt.timestamp())
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'Test Message'
            }
        },
        MessageBody=json.dumps(info), # Should be passed as str
        MessageGroupId="TestMsgGroupId",
        MessageDeduplicationId=sys.get('TransId')
    )
    msgId = response['MessageId']
    print(queue)

    return {
        'statusCode': 200,
        'body': json.dumps(msgId + ', ' + time_call)
    }
