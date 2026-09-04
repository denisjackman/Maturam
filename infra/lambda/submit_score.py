'''
    submit_score: validates a run result and writes it to the leaderboard table
'''
import json
import os
import time
import uuid

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

secrets_client = boto3.client("secretsmanager")
_cached_secret = None

REQUIRED_FIELDS = ("player", "score", "xp", "depth", "turns")


def _expected_secret():
    global _cached_secret
    if _cached_secret is None:
        response = secrets_client.get_secret_value(SecretId=os.environ["API_SECRET_ARN"])
        _cached_secret = response["SecretString"]
    return _cached_secret


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def handler(event, _context):
    '''
        POST /scores - validate an incoming score and record it
    '''
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    if headers.get("x-api-key") != _expected_secret():
        return _response(401, {"error": "unauthorized"})

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "invalid JSON body"})

    missing = [f for f in REQUIRED_FIELDS if f not in body]
    if missing:
        return _response(400, {"error": f"missing fields: {', '.join(missing)}"})

    player = str(body["player"]).strip()[:32]
    if not player:
        return _response(400, {"error": "player must not be empty"})

    try:
        score = int(body["score"])
        xp = int(body["xp"])
        depth = int(body["depth"])
        turns = int(body["turns"])
    except (TypeError, ValueError):
        return _response(400, {"error": "score, xp, depth, turns must be integers"})

    if score < 0 or score > 9_999_999_999:
        return _response(400, {"error": "score out of range"})

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
    sort_key = f"{score:010d}#{timestamp}#{uuid.uuid4()}"

    table.put_item(Item={
        "pk": "GLOBAL",
        "sk": sort_key,
        "player": player,
        "score": score,
        "xp": xp,
        "depth": depth,
        "turns": turns,
        "timestamp": timestamp,
    })

    return _response(201, {
        "player": player,
        "score": score,
        "timestamp": timestamp,
    })
