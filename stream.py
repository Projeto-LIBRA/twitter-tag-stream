import requests
import json
import boto3

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = ""
queue_sqs_url = ""
aws_key_id = ""
aws_secret_id = ""

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def send_to_sqs_queue(message):

    # Create SQS client
    sqs = boto3.client('sqs', aws_access_key_id=aws_key_id, aws_secret_access_key=aws_secret_id , region_name='sa-east-1')

    queue_url = queue_sqs_url

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageBody=message
    )

    print(response['MessageId'])
    print(message)
    print("------------------------------------")

def get_stream():

    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=conversation_id,created_at&expansions=author_id", auth=bearer_oauth, stream=True
    )

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    for response_line in response.iter_lines():

        if response_line:
            tweet_info = {}
            json_response = json.loads(response_line)

            if(json_response["data"]["author_id"] != "1559321348136108034"):

                tweet_info["conversation_id"] = json_response["data"]["conversation_id"]
                tweet_info["tag_created_at"] = json_response["data"]["created_at"]
                tweet_info["tag_id"] = json_response["data"]["id"]

                send_to_sqs_queue(json.dumps(tweet_info))

def main():

    get_stream()

if __name__ == "__main__":
    main()
