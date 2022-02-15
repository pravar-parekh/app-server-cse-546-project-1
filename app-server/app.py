from urllib import response
import boto3, json

sqs = boto3.client("sqs")
request_queue_url = 'https://sqs.us-east-1.amazonaws.com/547230687929/Request_Queue'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/547230687929/Response_Queue'

def send_message():

    message = {"key": "testing1234"}
    response = sqs.send_message(
        QueueUrl=response_queue_url,
        MessageBody=json.dumps(message)
    )
    print(response)

def receive_message():
    response = sqs.receive_message(
        QueueUrl=request_queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
    )

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {message_body}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")
        send_message()
        delete_message(message['ReceiptHandle'])

def delete_message(receipt_handle):
    response = sqs.delete_message(
        QueueUrl=request_queue_url,
        ReceiptHandle=receipt_handle,
    )
    print(response)

if __name__ == "__main__":
    receive_message()