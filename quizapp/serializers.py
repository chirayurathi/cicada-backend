from rest_framework import serializers
from .models import *

class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__'
        
class TeamSerializer(serializers.ModelSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())
    class Meta:
        model = Team
        fields = ['id','username','password','track','score']
        extra_kwargs = {
            'password':{'write_only':True},
            'id':{'read_only':True},
            'score':{'read_only':True},
            }
        depth = 1
        
    def create(self, validated_data):
        print(validated_data)
        user = Team.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'

class GetTeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many = True, source = 'player')
    class Meta:
        model = Team
        fields = ['id','username','track','score','players']

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):

        remove = kwargs.pop('remove', None)

        super(QuestionSerializer, self).__init__(*args, **kwargs)

        if remove is not None:
            for field_name in remove:
                self.fields.pop(field_name)

class CheckQuestionSerializer(serializers.ModelSerializer):
    question_no = serializers.IntegerField(validators=[], required = False)
    class Meta:
        model = Question
        fields = '__all__'
        validators = []

class GetTrackSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many= True, source = 'question')
    class Meta:
        model = Track
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {
            'timestamp':{'read_only':True},
            'is_correct':{'read_only':True},
        }
