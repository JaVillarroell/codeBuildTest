import json
import boto3
import os
from boto3.dynamodb.conditions import Key

table_name = os.environ['MOVIE_THEATER_TABLE']
dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table(table_name)

def getClientMovies(event, context):
  print(json.dumps(event));
  clientID = event['pathParameters']['clientID']
  response = table.query(
      KeyConditionExpression = Key('pk').eq("client_"+clientID)
      )
  items = response['Items']
  print(items)
  return {
      'statusCode': 200,
      'body': json.dumps(items)
  }
def putClients(event, context):
    print(json.dumps(event));
    movieID = event['pathParameters']['movieID']
    roomID = event['pathParameters']['roomID']
    bodyObj = json.loads(event["body"])
    date = event["queryStringParameters"]["date"]
    
    room = table.get_item(
    Key = {
        'pk': "room_" + roomID + "_" + date,
        'sk':'information'
      })
    availableSeats = room['Item']['AvailableSeats']
    if len(bodyObj["Clients"]) > int(availableSeats) :
      response = "Too many people too little seats :( "
      print(response)
    else:
      for client in bodyObj["Clients"]:
        table.put_item(
          Item = {
            'pk':"movie_" + movieID + "_" + date + "_room_" + roomID,
            'sk': 'client_' + client
          })
      table.put_item(
        Item = {
            'pk':"room_" + roomID + "_" + date,
            'sk':'information',
            'AvailableSeats' : int(availableSeats) - len(bodyObj["Clients"]),
            '3D' :room['Item']['3D']
        })
      response = "success"
      print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response)}