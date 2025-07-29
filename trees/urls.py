from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.CustomLoginView.as_view(template_name='trees/login.html'), name='login'),
  path('my-trees/', views.UserPlantedTreeView.as_view(), name='user-trees'),
  path('account-trees/', views.AccountPlantedTreeView.as_view(), name='account-trees'),
  path('planted/<int:pk>/', views.PlantedTreeDetailView.as_view(), name='planted-tree-detail'),
  path('plant-tree/', views.PlantedTreeCreateView.as_view(), name='plant-tree'),
  path('api/my-trees/', views.UserPlantedTreeAPIView.as_view(), name='api-user-trees'),
]
