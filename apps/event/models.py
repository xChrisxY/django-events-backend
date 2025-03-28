from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organizer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="organized_events",
        verbose_name="Organizador"
    )
    participants = models.ManyToManyField(
        User,
        related_name="participating_events",
        verbose_name="Participantes",
        blank=True
    )

    def __str__(self):
        return self.name

        
class EventImage(models.Model):
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Evento"
    )
    image = models.ImageField(upload_to="event_images/")
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen para {self.event.name}"

class AudioNote(models.Model):
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="audio_notes",
        verbose_name="Evento"
    )
    audio_file = models.FileField(upload_to="event_audio_notes/")
    title = models.CharField(max_length=100, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de audio para {self.event.name}: {self.title}"
    
    
    



