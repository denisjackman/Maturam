'''
    top_scores: returns the highest-scoring runs recorded so far
'''
import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

DEFAULT_LIMIT = 10
MAX_LIMIT = 100


def handler(event, _context):
    '''
        GET /scores/top?limit=N - the top N scores, best first
    '''
    params = event.get("queryStringParameters") or {}
    try:
        limit = int(params.get("limit", DEFAULT_LIMIT))
    except ValueError:
        limit = DEFAULT_LIMIT
    limit = max(1, min(limit, MAX_LIMIT))

    response = table.query(
        KeyConditionExpression=Key("pk").eq("GLOBAL"),
        ScanIndexForward=False,
        Limit=limit,
    )

    scores = [
        {
            "player": item["player"],
            "score": int(item["score"]),
            "xp": int(item["xp"]),
            "depth": int(item["depth"]),
            "turns": int(item["turns"]),
            "timestamp": item["timestamp"],
        }
        for item in response.get("Items", [])
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(scores),
    }
