from django.urls import path
from .views import EducationList, EducationDetail

urlpatterns = [
    path('', EducationList.as_view(), name='education-list'),
    path('<int:pk>/', EducationDetail.as_view(), name='education-detail'),
]