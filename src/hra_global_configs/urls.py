from django.urls import path
from .views import GlobalConfigList, GlobalConfigDetail

urlpatterns = [
    path('', GlobalConfigList.as_view(), name='global-config-list'),
    path('<int:pk>/', GlobalConfigDetail.as_view(), name='global-config-detail'),
]