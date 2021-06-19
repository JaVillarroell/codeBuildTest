import json
import boto3
import os

table_name = os.environ['MOVIE_THEATER_TABLE']
dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table(table_name)

def getRoom(event, context):
  print(json.dumps(event));
  roomID = event['pathParameters']['roomID']
  date = event["queryStringParameters"]["date"]
  response = table.get_item(
    Key = {
        'pk': "room_" + roomID + "_" + date,
        'sk':'information'
      })
  item = response['Item']
  print(item)
  return {
      'statusCode': 200,
      'body': json.dumps(item)
  }