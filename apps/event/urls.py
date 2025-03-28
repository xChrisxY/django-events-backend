from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventImageViewSet, AudioNoteViewSet

# Creamos un router para las vistas basadas ViewSets
router = DefaultRouter()

router.register(r'events', EventViewSet, basename='event')
router.register(r'events', EventImageViewSet, basename='event-image')
router.register(r'events', AudioNoteViewSet, basename='event-audio')

urlpatterns = [
    path('', include(router.urls))
]
