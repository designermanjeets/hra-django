from django.urls import path
from .views import ExperienceList, ExperienceDetail

urlpatterns = [
    path('experiences/', ExperienceList.as_view(), name='experience-list'),
    path('experiences/<int:pk>/', ExperienceDetail.as_view(), name='experience-detail'),
]