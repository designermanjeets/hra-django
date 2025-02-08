from django.urls import path
from .views import EducationList, EducationDetail

urlpatterns = [
    path('educations/', EducationList.as_view(), name='education-list'),
    path('educations/<int:pk>/', EducationDetail.as_view(), name='education-detail'),
]