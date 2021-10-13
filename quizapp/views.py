from copy import error
from django.contrib.auth import authenticate
from django.http import response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .serializers import *

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({
            'success':False,
            'message': 'Please provide both username and password'
            },
            status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({
            'success':False,
            'error': 'Invalid Credentials'
            }, 
            status=HTTP_404_NOT_FOUND)

    try:
        token = Token.objects.get(user=user)
        token.delete().save()
        token = Token.objects.create(user=user).save()
    except:
        Token.objects.create(user=user).save()
    token = Token.objects.get(user=user)
    response = Response()
    response.data = {
        'success':True,
        'message': "Login Successful",
        'data':{
            'team':TeamSerializer(instance=user).data,
            'token': token.key,
            }
        }
    response.status = HTTP_200_OK
    return response

@api_view(['POST'])
@permission_classes((IsAdminUser,))
def registerTeam(request):
    serializer = TeamSerializer(data = request.data)
    response = Response()

    if serializer.is_valid():
        serializer.save()
        response.data = {
        "success":True,
        "message":"Team added Sucessfully.",
        'data': serializer.data
        }
        response.status = HTTP_200_OK

    else:
        response.data = {
            'success': False,
            'message': serializer.errors[list(serializer.errors.keys())[0]][0],
            'errors': serializer.errors
        }
        response.status = HTTP_400_BAD_REQUEST

    return response

@api_view(['PUT'])
@permission_classes((IsAdminUser,))
def updateTeam(request,id):
    response = Response()

    try:
        team = Team.objects.get(pk=id)
        serializer = TeamSerializer(team,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response.data = {
            "success":True,
            "message":'Team updated Sucessfully.',
            'data': serializer.data
            }
            response.status = HTTP_200_OK

        else:
            response.data = {
                'success': False,
                'message': serializer.errors[list(serializer.errors.keys())[0]][0],
                'errors': serializer.errors
            }
            response.status = HTTP_400_BAD_REQUEST
    except:
        response.data = {
            'success':False,
            "message":f"Team {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response

@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def deleteTeam(request,id):
    response = Response()
    try:
        team = Team.objects.get(pk=id)
        team.delete()
        response.data = {
            'success':True,
            'message':f'Team {id} deleted Successfully.'
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            "message":f"Team {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getTeam(request,id):
    response = Response()
    try:
        team = Team.objects.get(pk=id)
        serializer = GetTeamSerializer(instance=team)
        response.data = {
            'success':True,
            'message':"Team Exists.",
            'data': serializer.data
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            'message':"Team Does Not Exist"
        }
        response.status = HTTP_404_NOT_FOUND
    
    return response

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def getAllTeams(request):
    response = Response()
    try:
        teams = Team.objects.all()
        serializer = GetTeamSerializer(teams, many= True)
        response.data = {
            'success':True,
            'message':"All Teams Data",
            'data': serializer.data
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            'message':"Some error occoured"
        }
        response.status = HTTP_404_NOT_FOUND
    
    return response

@api_view(['POST'])
@permission_classes((IsAdminUser,))
def addPlayer(request):
    serializer = PlayerSerializer(data = request.data)
    response = Response()

    if serializer.is_valid():
        serializer.save()
        response.data = {
        "success":True,
        "message":"Player added Sucessfully.",
        'data': serializer.data
        }
        response.status = HTTP_200_OK

    else:
        response.data = {
            'success': False,
            'message': serializer.errors[list(serializer.errors.keys())[0]][0],
            'errors': serializer.errors
        }
        response.status = HTTP_400_BAD_REQUEST

    return response

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getPlayer(request,id):
    response = Response()
    try:
        player = Player.objects.get(pk=id)
        serializer = PlayerSerializer(instance=player)
        response.data = {
            'success':True,
            'message':"Player Exists.",
            'data': serializer.data
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            'message':"Team Does Not Exist"
        }
        response.status = HTTP_404_NOT_FOUND
    
    return response


@api_view(['PUT'])
@permission_classes((IsAdminUser,))
def updatePlayer(request,id):
    response = Response()

    try:
        player = Player.objects.get(pk=id)
        serializer = PlayerSerializer(player,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response.data = {
            "success":True,
            "message":'Player updated Sucessfully.',
            'data': serializer.data
            }
            response.status = HTTP_200_OK

        else:
            response.data = {
                'success': False,
                'message': serializer.errors[list(serializer.errors.keys())[0]][0],
                'errors': serializer.errors
            }
            response.status = HTTP_400_BAD_REQUEST
    except:
        response.data = {
            'success':False,
            "message":f"Player {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response

@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def deletePlayer(request,id):
    response = Response()
    try:
        player = Player.objects.get(pk=id)
        player.delete()
        response.data = {
            'success':True,
            'message':f'Player {id} deleted Successfully.'
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            "message":f"Player {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def addTrack(request):
    serializer = TrackSerializer(data = request.data)
    response = Response()

    if serializer.is_valid():
        serializer.save()
        response.data = {
        "success":True,
        "message":"Track added Sucessfully.",
        'data': serializer.data
        }
        response.status = HTTP_200_OK

    else:
        response.data = {
            'success': False,
            'message': serializer.errors[list(serializer.errors.keys())[0]][0],
            'errors': serializer.errors
        }
        response.status = HTTP_400_BAD_REQUEST

    return response

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def getTrack(request,id):
    response = Response()
    try:
        track = Track.objects.get(pk=id)
        serializer = GetTrackSerializer(instance=track)
        response.data = {
            'success':True,
            'message':"Track Exists.",
            'data': serializer.data
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            'message':"Track Does Not Exist"
        }
        response.status = HTTP_404_NOT_FOUND
    
    return response


@api_view(['PUT'])
@permission_classes((IsAdminUser,))
def updateTrack(request,id):
    response = Response()

    try:
        track = Track.objects.get(pk=id)
        serializer = TrackSerializer(track,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response.data = {
            "success":True,
            "message":'Track updated Sucessfully.',
            'data': serializer.data
            }
            response.status = HTTP_200_OK

        else:
            response.data = {
                'success': False,
                'message': serializer.errors[list(serializer.errors.keys())[0]][0],
                'errors': serializer.errors
            }
            response.status = HTTP_400_BAD_REQUEST
    except:
        response.data = {
            'success':False,
            "message":f"Track {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response

@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def deleteTrack(request,id):
    response = Response()
    try:
        track = Track.objects.get(pk=id)
        track.delete()
        response.data = {
            'success':True,
            'message':f'Track {id} deleted Successfully.'
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            "message":f"Track {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def getAllTracks(request):
    response = Response()
    try:
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many= True)
        response.data = {
            'success':True,
            'message':"All Track Data",
            'data': serializer.data
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            'message':"Some error occoured"
        }
        response.status = HTTP_404_NOT_FOUND
    
    return response

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def test(request):
    response = Response()
    response.data = {
        'success':True,
        "message":"new token works"
    }
    response.status = HTTP_200_OK
    return response
