from django.urls import path
from . import views

urlpatterns = [
    path('library', views.library_list, name='library'),
    path('library/framework/<slug:slug>', views.framework_detail, name='framework_detail'),
]
