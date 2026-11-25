from django.urls import path
from . import views
from .views import get_habits
from .views import login_view
from .views import decrypt_data
from .views import export_data, export_encrypted_data

urlpatterns = [

    path('api/habit/', views.create_habit),       
    path('api/habit/all/', views.get_habits),      
    path('api/habit/<int:id>/', views.get_habit),  
    path('api/habit/delete/<int:id>/', views.delete_habit),  
    path('documentation/download/', views.download_documentation),
     path('', views.home),
     path('api/habit/update/<int:id>/', views.update_habit),
     path('api/habit/<int:id>/', views.get_habit),
     path('api/habit/count/', views.habit_count),
     path('api/habit/export/', views.export_data),
     path('api/habit/reset/', views.reset_storage),
     path('login/', login_view, name='login'),
      path('habits/', get_habits),
     path('api/habit/export-encrypted/', export_encrypted_data),
     path('api/habit/decrypt/', decrypt_data),
     path('api/habit/search/', views.search_habits),
]

