from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Habit.urls')),
     path('api/', include('Habit.urls')),
]