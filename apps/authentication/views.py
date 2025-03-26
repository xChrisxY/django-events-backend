from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer 

    def get_queryset(self):
        # Permisos personalizados
        if self.action in ['create', 'reset_password']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        # Seleccionar el serializador según la acción
        if self.action == 'create':
            return UserRegistrationSerializer
        return self.serializer_class

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # Obtenemos los datos del perfil para la respuesta
            profile_serializer = UserProfileSerializer(user)       
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def profile(self, request):

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

        
    @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)