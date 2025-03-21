from django.db import models
from django.contrib.auth.models import User
# Create your models here.




# Modelo de usuario personalizado
class User_Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_Data')
    location = models.CharField(max_length=255, blank=True, null=True)
    is_professional = models.BooleanField(default=False)  # Identificar si es un profesional de salud mental

    def __str__(self):
        return self.username

# Modelo de perfil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferences = models.TextField(blank=True, null=True)  # Campo para almacenar preferencias del usuario

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Modelo de citas
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    title = models.CharField(max_length=100, default='--')
    professional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_appointments')
    date = models.DateTimeField(null=False)  # Fecha seleccionada por el usuario
    datecompleted = models.DateTimeField(null=True, blank=True)  # Fecha opcional
    description = models.TextField(blank=True, null=True)  # Descripción opcional
    important = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username} - {self.date}"

# Modelo de seguimiento del estado de ánimo
class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=50)  # Ej: "Feliz", "Triste", "Ansioso"
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Estado de ánimo de {self.user.username} el {self.date}"

# Modelo de recursos de autoayuda
class SelfHelpResource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.CharField(max_length=50, choices=[('article', 'Artículo'), ('video', 'Video'), ('exercise', 'Ejercicio')])
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

# Modelo de notificaciones
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.message}"

# Modelo para gestionar usuarios y recursos por parte de administradores
class AdminPanel(models.Model):
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_panel')
    managed_users = models.ManyToManyField(User, related_name='managed_by', blank=True)

    def __str__(self):
        return f"Panel de administración de {self.admin_user.username}"
