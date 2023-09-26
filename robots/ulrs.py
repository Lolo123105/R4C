from django.urls import path
from .views import ApiView, ApiIdView

app_name = 'api'

urlpatterns = [
    path('api/', ApiView, name='api_all'),
    path('api/<int:id>/', ApiIdView, name='api_id')
]
