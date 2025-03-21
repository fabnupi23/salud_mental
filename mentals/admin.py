from django.contrib import admin
from .models import User_Data, Profile, Appointment, MoodLog, SelfHelpResource, Notification, AdminPanel

# Register your models here.


admin.site.register(User_Data)
admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(MoodLog)
admin.site.register(SelfHelpResource)
admin.site.register(Notification)
admin.site.register(AdminPanel)