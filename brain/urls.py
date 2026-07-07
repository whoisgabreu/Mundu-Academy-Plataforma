from django.urls import path
from . import views

urlpatterns = [
    path('my-brain', views.my_brain, name='my_brain'),
]
