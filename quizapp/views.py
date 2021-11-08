from django.contrib.auth import authenticate
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
from django.db.models import F

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
    print(request.data)
    serializer = TeamSerializer(data = request.data)
    response = Response()

    if serializer.is_valid():
        newTeam = serializer.save()
        # newTeam = Team.objects.create_user(username=request.data.get("username"),password=request.data.get("password"),track=request.data.get("track"))
        response.data = {
        "success":True,
        "message":"Team added Sucessfully.",
        'data': TeamSerializer(newTeam).data
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

def addLastQuestion(data):
    response = Response()
    print(data)
    data["question_no"] = Question.objects.filter(track__id = data["track"]).count() + 1
    serializer = QuestionSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        response.data = {
        "success":True,
        "message":"Question added Sucessfully.",
        'data': serializer.data
        }
        response.status = HTTP_200_OK
    else:
        response.data = {
            'success': False,
            'message': "Backend logical error on adding question at the end.",
            'errors': serializer.errors
        }
        response.status = HTTP_400_BAD_REQUEST
    return response

def addIndexedQuestion(data):
    response = Response()
    if(data["question_no"] < 0 or data["question_no"] > Question.objects.filter(track__id = data["track"]).count() + 1):
        response.data = {
            'success':False,
            'message':"Question Position Out Of Range.",
        }
        response.status = HTTP_400_BAD_REQUEST
        return response
    try:
        Question.objects.filter(track__id = data["track"], question_no__gte = data["question_no"]).update(question_no = F('question_no')+1 )
    except Exception as ex:
        response.data = {
            'success':False,
            'message':f'Error while updating preceeding questions, error type: {type(ex).__name__}',
        }
        response.status = HTTP_400_BAD_REQUEST
        return response
    serializer = QuestionSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        response.data = {
        "success":True,
        "message":"Question added Sucessfully.",
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

@api_view(['POST'])
@permission_classes((IsAdminUser,))
def addQuestion(request):
    data = request.data
    response = Response()
    checkSerializer = CheckQuestionSerializer(data=data)
    if checkSerializer.is_valid():
        if not data.get("question_no"):
            response = addLastQuestion(data)
        else:
            response = addIndexedQuestion(data)
    else:
        print("error here")
        response.data = {
            'success': False,
            'message': checkSerializer.errors[list(checkSerializer.errors.keys())[0]][0],
            'errors': checkSerializer.errors
        }
        response.status = HTTP_400_BAD_REQUEST

    return response

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def getQuestion(request,id):
    response = Response()
    try:
        question = Question.objects.get(pk=id)
        serializer = QuestionSerializer(instance=question)
        response.data = {
            'success':True,
            'message':"Question Exists.",
            'data': serializer.data
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            'message':"Question Does Not Exist"
        }
        response.status = HTTP_404_NOT_FOUND
    
    return response 

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getCurrentQuestion(request):
    # try:
    question = calcTeamQuestion(request.user)
    print(question)
    print(request.user)
    response = Response()
    response.data = {
        'success':True,
        'message':"question GET successful." if question else "You have already completed the test",
        'data':{
            "current_question":QuestionSerializer(question, remove=['correct_answer','hint','super_hint']).data,
            "completed":False if question else True
        }
    }
    # except Exception as ex:
    #     response.data = {
    #         'success':False,
    #         'message':f'An Error Occoured of type {type(ex).__name__}'
    #     }
    #     response.status = HTTP_400_BAD_REQUEST
    return response

def updateIndexedQuestion(instance,data):
    response = Response()
    if(data["question_no"] < 0 or data["question_no"] > Question.objects.filter(track__id = data["track"]).count()):
        response.data = {
            'success':False,
            'message':"Question Position Out Of Range.",
        }
        response.status = HTTP_400_BAD_REQUEST
        return response
    try:
        ins = Question.objects.get(id=instance.id)
        ins.question_no = -1
        ins.save()
        if(instance.question_no > data["question_no"]):
            Question.objects.filter(track__id = data["track"], question_no__gte = data["question_no"], question_no__lt = instance.question_no).update(question_no = F('question_no')+1 )
            newIns = Question.objects.get(id=instance.id)
            newSerializer = QuestionSerializer(newIns, data = data)
            if newSerializer.is_valid():
                newSerializer.save()
                response.data = {
                    "success":True,
                    "message":"Question added Sucessfully.",
                    'data': newSerializer.data
                }
                response.status = HTTP_200_OK
                return response
            else:
                print("error here")
                response.data = {
                    'success':False,
                    'message': newSerializer.errors[list(newSerializer.errors.keys())[0]][0],
                    'errors': newSerializer.errors
                }
                response.status = HTTP_400_BAD_REQUEST
                return response
        elif (instance.question_no < data["question_no"]):
            Question.objects.filter(track__id = data["track"], question_no__lte = data["question_no"], question_no__gt = instance.question_no).update(question_no = F('question_no') - 1 )
            newIns = Question.objects.get(id=instance.id)
            newSerializer = QuestionSerializer(newIns, data = data)
            if newSerializer.is_valid():
                newSerializer.save()
                response.data = {
                    "success":True,
                    "message":"Question added Sucessfully.",
                    'data': newSerializer.data
                }
                response.status = HTTP_200_OK
                return response
            else:
                response.data = {
                    'success':False,
                    'message': newSerializer.errors[list(newSerializer.errors.keys())[0]][0],
                    'errors': newSerializer.errors
                }
                response.status = HTTP_400_BAD_REQUEST
                return response
        else:
            ins = Question.objects.get(pk = instance.id)
            serializer = QuestionSerializer(ins, data = data)
            if serializer.is_valid():
                serializer.save()
                response.data = {
                "success":True,
                "message":"Question added Sucessfully.",
                'data': serializer.data
                }
                response.status = HTTP_200_OK
                return response
            else:
                response.data = {
                    'success': False,
                    'message': serializer.errors[list(serializer.errors.keys())[0]][0],
                    'errors': serializer.errors
                }
                response.status = HTTP_400_BAD_REQUEST
                return response
    except Exception as ex:
        response.data = {
            'success':False,
            'message':f'Error while updating preceeding questions, error type: {type(ex).__name__}',
        }
        response.status = HTTP_400_BAD_REQUEST
        return response

@api_view(['PUT'])
@permission_classes((IsAdminUser,))
def updateQuestion(request,id):
    response = Response()
    try:
        question = Question.objects.get(pk=id)
        serializer = CheckQuestionSerializer(question,data=request.data)
        if serializer.is_valid():
            if request.data.get("question_no"):
                response = updateIndexedQuestion(question,request.data)
            else:
                response.data = {
                    'success': False,
                    'message': "Field Question no. required.",
                }
            response.status = HTTP_400_BAD_REQUEST
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
            "message":f"Question {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response

@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def deleteQuestion(request,id):
    response = Response()
    try:
        question = Question.objects.get(pk=id)
        question.delete()
        Question.objects.filter(question_no__gte = question.question_no).update(question_no = F('question_no') -1 )
        response.data = {
            'success':True,
            'message':f'Question {id} deleted Successfully.'
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            "message":f"Question {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response

@api_view(['POST'])
@permission_classes((IsAdminUser,))
def addAnswerAdmin(request):
    serializer = AnswerSerializer(data = request.data)
    response = Response()
    if serializer.is_valid():
        question = Question.objects.get(pk = request.data["question"])
        is_correct = True if request.data["given_answer"] == question.correct_answer else False
        serializer.save(is_correct = is_correct)
        response.data = {
        "success":True,
        "message":"Answer added Sucessfully.",
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

def calcTeamQuestion(team):
    return Question.objects.filter( track = team.track,  ).exclude( answer__in = Answer.objects.filter(is_correct = True, team = team) ).order_by('question_no').first()

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def addAnswerUser(request):
    try:
        response = Response()
        team = request.user
        given_answer = request.data.get("answer")
        if given_answer is None:
            response.data = {
                'success':False,
                'message':"given_answer field is required."
            }
            response.status = HTTP_400_BAD_REQUEST
            return response
        question = calcTeamQuestion(team)
        is_correct = question.correct_answer == given_answer
        answer = Answer.objects.create(team = team, given_answer = given_answer, question = question, is_correct = is_correct)
        if is_correct:
            next_question = calcTeamQuestion(team)
            questionData = QuestionSerializer(next_question, remove = ['correct_answer','hint','super_hint']).data if next_question else None
            response.data = {
                'success':True,
                'message':"Congratulations! Your answer was correct.",
                'data':{
                    'answer':AnswerSerializer(answer).data,
                    'next_question': questionData,
                    'completed': False if next_question else True
                }
            }
        else:
            response.data = {
                'success':True,
                'message':'Sorry, The answer was Incorrect.',
                'data':{
                    'answer':AnswerSerializer(answer).data,
                    'completed':False
                }
            }
        response.status = HTTP_200_OK
    except Exception as ex:
        response.data = {
            'success':False,
            'message':f'An Error Occoured of type {type(ex).__name__}'
        }
        response.status = HTTP_400_BAD_REQUEST
    return response

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def getAnswersByQuery(request):
    response = Response()
    try:
        id = request.GET.get("id")
        team = request.GET.get("team")
        correct_only = request.GET.get("correct_only")
        question = request.GET.get("question")
        track = request.GET.get("track")
        allAnswers = Answer.objects.filter()
        if id is not None:
            print(id)
            allAnswers = allAnswers.filter(pk=id)
        if team is not None:
            allAnswers = allAnswers.filter(team = int(team))
        if correct_only is not None and correct_only == "yes":
            allAnswers = allAnswers.filter(is_correct = True)
        if question is not None:
            allAnswers = allAnswers.filter(question = int(question))
        if track is not None:
            allAnswers = allAnswers.filter(question__track = int(track))
        response.data = {
            'success':True,
            'message':"Answers lookup  successful.",
            'data':AnswerSerializer(allAnswers,many=True).data
        }
    except Exception as ex:
        response.data = {
            'success':False,
            'message':f'An Error Occoured of type {type(ex).__name__}'
        }
        response.status = HTTP_400_BAD_REQUEST
    return response

        
    
@api_view(['PUT'])
@permission_classes((IsAdminUser,))
def updateAnswer(request,id):
    response = Response()
    try:
        answer = Answer.objects.get(pk=id)
    except:
        response.data = {
            'success':False,
            "message":f"Team {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND
        return response
    serializer = AnswerSerializer(answer,data = request.data)
    if serializer.is_valid():
        is_correct = answer.question.correct_answer == request.data["given_answer"]
        serializer.save(is_correct=is_correct)
        response.data = {
            'success':True,
            'message':f'Answer {answer.id} Updated.',
            'data':serializer.data
        }
        response.status = HTTP_200_OK
    else:
        response.data = {
            'success':False,
            'message':serializer.errors[list(serializer.errors.keys())[0]][0],
            'errors':serializer.errors
        }
        response.status = HTTP_400_BAD_REQUEST
    return response

@api_view(['DELETE'])
@permission_classes((IsAdminUser,))
def deleteAnswer(request,id):
    response = Response()
    try:
        answer = Answer.objects.get(pk=id)
        answer.delete()
        response.data = {
            'success':True,
            'message':f'Answer {id} deleted Successfully.'
        }
        response.status = HTTP_200_OK
    except:
        response.data = {
            'success':False,
            "message":f"Answer {id} Does Not Exist."
        }
        response.status = HTTP_404_NOT_FOUND

    return response

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getHint(request):
    response = Response()
    question = calcTeamQuestion(request.user)
    if not question:
        response.data = {
            'success':False,
            "message":f"You have already completed the test."
        }
        response.status = HTTP_404_NOT_FOUND
        return response

    usedhint = UsedHints.objects.filter(team = request.user, question = question)
    if not usedhint:
        UsedHints.objects.create(team = request.user, question = question)
    response.data = {
        'success':True,
        "message":question.hint,
    }
    response.status = HTTP_200_OK
    return response