import json
import logging
import boto3
import datetime
import dynamo

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
table_name = 'article'


def create(event, context):
    logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating articles."
    }

    article_str = event['body']
    article = json.loads(article_str)
    current_timestamp = datetime.datetime.now().isoformat()
    article['createdAt'] = current_timestamp

    res = dynamodb.put_item(
        TableName=table_name, Item=dynamo.to_item(article))

    # If creation is successful
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 201,
        }

    return response


def get(event, context):
    logger.info(f'Incoming request is: {event}')
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting article."
    }

    article_id = event['pathParameters']['articleId']

    article_query = dynamodb.get_item(
        TableName=table_name, Key={'id': {'N': article_id}})

    if 'Item' in article_query:
        article = article_query['Item']
        logger.info(f'article is: {article}')
        response = {
            "statusCode": 200,
            "body": json.dumps(dynamo.to_dict(article))
        }

    return response


def all(event, context):
    # Set the default error response
    logger.info(f'Incoming request is: {event}')
    logger.error(f'Incoming request is: {event}')
    logger.warning(f'Incoming request is: {event}')
    response = {
        "statusCode": 500,
        "body": "An error occured while getting all articles."
    }

    scan_result = dynamodb.scan(TableName=table_name)['Items']

    articles = []

    for item in scan_result:
        articles.append(dynamo.to_dict(item))

    response = {
        "statusCode": 200,
        "body": json.dumps(articles)
    }

    return response


def update(event, context):
    logger.info(f'Incoming request is: {event}')

    article_id = event['pathParameters']['articleId']

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": f"An error occured while updating article {article_id}"
    }

    article_str = event['body']

    article = json.loads(article_str)

    res = dynamodb.update_item(
        TableName=table_name,
        Key={
            'id': {'N': article_id}
        },
        UpdateExpression="set content=:c, author=:a, updatedAt=:u",
        ExpressionAttributeValues={
            ':c': dynamo.to_item(article['content']),
            ':a': dynamo.to_item(article['author']),
            ':u': dynamo.to_item(datetime.datetime.now().isoformat())
        },
        ReturnValues="UPDATED_NEW"
    )

    # If updation is successful for article
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 200,
        }

    return response


def delete(event, context):
    logger.info(f'Incoming request is: {event}')

    article_id = event['pathParameters']['articleId']

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": f"An error occured while deleting article {article_id}"
    }

    res = dynamodb.delete_item(TableName=table_name, Key={
                               'id': {'N': article_id}})

    # If deletion is successful for article
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 204,
        }
    return response
