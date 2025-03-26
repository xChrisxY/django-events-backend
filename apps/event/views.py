from rest_framework import viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Event, EventImage, AudioNote
from .serializers import EventSerializer, EventImageSerializer, AudioNoteSerializer
from django.db.models import Q

class EventViewSet(viewsets.ModelViewSet):
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):

        """
        Permisos personalizados
        """

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Solo usuarios autenticados pueden crear/modificar eventos
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):

        """
        Sobreescribimos el método para mostrar los eventos organizados o en los que participa el cliente.
        """

        user = self.request.user
        if user.is_authenticated:

            events = Event.objects.filter(
                Q(organizer=user) | Q(participants=user)
            ).distinct()
            return events

        return Event.objects.none()
