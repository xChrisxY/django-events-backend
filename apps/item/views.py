from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Item, ItemList
from apps.event.models import Event
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        # Personalizamos los permisos
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        # Filtrar por elementos por eventos si se proporciona
        event_id = self.request.query_params.get('event_id', None)
        print(f"El evento es -> {event_id}")
        if event_id:
            items = Item.objects.filter(item_list__event_id=event_id)
            return items
        return Item.objects.none()

        
    def create(self, request, *args, **kwargs):
        # Personalizamos la creación de un elemento
        print(request.data)
        event_id = request.data.get('event_id')
        if not event_id:
            return Response({"error": "Se requiere un ID de evento."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
            item_list, _ = ItemList.objects.get_or_create(event=event)
        except Event.DoesNotExist:
            return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Añadimos el item a la lista del evento
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save(item_list=item_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)