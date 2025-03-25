from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, AudioNote, EventImage
from item.serializers import ItemListSerializer, ItemSerializer
from authentication.serializers import UserSerializer

class EventImageSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = EventImage,
        fields = ['id', 'image', 'caption', 'uploaded_at']
        read_only_fields = ['uploaded_at']
        
class AudioNoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AudioNote
        fields = ['id', 'audio_file', 'title', 'recorded_at']
        read_only_fields = ['recorded_at']

        
class EventSerializer(serializers.ModelSerializer):
    pass