import json
import boto3
import os
from boto3.dynamodb.conditions import Key

table_name = os.environ['MOVIE_THEATER_TABLE']
dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table(table_name)

def getMovie(event, context):
    path = event["path"]
    array_path = path.split("/")
    movieID = array_path[-1]
    
    response = table.get_item(
        Key = {
            'pk': "movie_" + movieID,
            'sk':'information'
        })
    item = response['Item']
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
def getRoomsSchedule(event, context):
    print(json.dumps(event));
    movieID = event['pathParameters']['movieID']
    date = event["queryStringParameters"]["date"]
    response = table.query(
        KeyConditionExpression = Key('pk').eq("movie_"+movieID+"_"+date)
        )
    items = response['Items']
    print(items)
    return {
        'status code': 200,
        'body': json.dumps(items)
    }
def getClients(event, context):
    print(json.dumps(event));
    movieID = event['pathParameters']['movieID']
    roomID =  event['pathParameters']['roomID'] 
    date = event["queryStringParameters"]["date"]
    response = table.query(
        KeyConditionExpression = Key('pk').eq("movie_"+movieID+"_"+date+"_room_"+roomID)
        )
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
def putMovieInfo(event, context):
    print(json.dumps(event));
    movieID = event['pathParameters']['movieID']
    bodyObj = json.loads(event["body"])
    response = table.put_item(
        Item = {
            'pk':"movie_" + movieID,
            'sk': 'information',
            'Title' : bodyObj['Title'],
            'Actors' : bodyObj['Actors'],
            'Year' : bodyObj['Year'],
        })
    return {
        'statusCode': 200,
        'body': json.dumps("success")}

