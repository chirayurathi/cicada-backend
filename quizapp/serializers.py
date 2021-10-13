from rest_framework import serializers
from .models import *

class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__'
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','password','username','track','score']
        extra_kwargs = {
            'password':{'write_only':True},
            'id':{'read_only':True},
            'score':{'read_only':True},
            }
        depth = 1
        
        def create(self, validated_data):
            user = super().create(validated_data)
            user.set_password(validated_data['password'])
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

class GetTrackSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many= True, source = 'question')
    class Meta:
        model = Track
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
