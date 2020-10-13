import json
from zeep import Client
import lxml
import boto3


def lambda_handler(event, context):
    print(event)
    records = event.get('Records')
    # Create SQS client
    sqs = boto3.client('sqs')
    queue = sqs.create_queue(QueueName="QueueForAPI.fifo",
                             Attributes={"FifoQueue": "True"})
    queue_url = queue.get('QueueUrl')
    for msg in records:
        msgId = msg.get('messageId')
        msgBody = msg.get('body')
        print(msgBody)
        print(type(msgBody))
        msgBody = json.loads(msgBody)
        isSuccess = msgBody.get('isSuccess')
        print(isSuccess)
        statement = None
        if(isSuccess):

            # Call soap here
            wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
            client = Client(wsdl=wsdl)
            result = client.service.Method1('Zeep', 'is cool')
            print(result)
            statement = 'Result from soap call: ' + str(result)

            receipt_handle = msg.get('receiptHandle')
            try:
                # Explicitly delete received message
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
            except Exception as e:
                pass
            print('Received and deleted message: %s' % msg)

        else:
            raise Exception('Throw error to failed msg processed - This message will be move to dead queue')
    if statement is not None:
        return {
            'statusCode': 200,
            'body': json.dumps(statement)
        }
    else:
        return {
            'statusCode': 500,
            'body': "{\"message\":\"Server error!\"}"
        }
    # response = sqs.receive_message(
    #     QueueUrl=queue_url,
    #     MaxNumberOfMessages=1,
    #     #ReceiveRequestAttemptId='string'
    # )
    # messages = response['Messages']
    #
    # for msg in messages:
    #     receipt_handle = msg['ReceiptHandle']
    #     print(msg)
    #     # Delete received message from queue
    #     sqs.delete_message(
    #         QueueUrl=queue_url,
    #         ReceiptHandle=receipt_handle
    #     )
    #     print('Received and deleted message: %s' % msg)

eventObj = {'Records': [{'messageId': '456c6a1a-2ba1-4f12-99e4-3357909ffb15',
                         'receiptHandle': 'AQEBuZWUFDGFLydVOpN8oT7DdVJiKGwmmEusP3J6mHji/w3vbL8Q5dzg0T5Qz0eBPLWuuDrTZ7FuaKF/NgzDd2gnoEN0MNqTk6VHONv2sHud/U4zvlQ1goYaACu7mNpbfMw8xgaOy6hYecwpvNuW5bDzKij32qAkPFYV+vWmnCkj2Sy74d5WPZEx9H+/oPqJuaccFQUtXCnMAicila//xQhhVjVuwVL2HQMliro8GjAflsQzCMLGyOSOteu8b09qKkzQbvhYBaBMJ3F85LYxq7zr7i7jZ6gQOUHTxYkRcNAUMls=',
                         'body': 'time call: 2020-09-28 04:19:24.917902',
                         'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1601266764924',
                                        'SequenceNumber': '18856668365530095616', 'MessageGroupId': 'TestMsgGroupId',
                                        'SenderId': 'AROA3E5YUCBK336QEB6WW:test-lxml-zeep',
                                        'MessageDeduplicationId': '1601266764',
                                        'ApproximateFirstReceiveTimestamp': '1601266764924'}, 'messageAttributes': {
        'Title': {'stringValue': 'The Whistler', 'stringListValues': [], 'binaryListValues': [], 'dataType': 'String'}},
                         'md5OfMessageAttributes': 'f4ba90390ad3f80d43ce8a9e4a4abfd6',
                         'md5OfBody': '2255971e430e60ffd1b83644c8cb0415', 'eventSource': 'aws:sqs',
                         'eventSourceARN': 'arn:aws:sqs:ap-southeast-1:766501982293:TestQueue.fifo',
                         'awsRegion': 'ap-southeast-1'}]}
