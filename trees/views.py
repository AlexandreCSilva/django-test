from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from rest_framework import permissions, generics
from .models import PlantedTree
from .serializers import PlantedTreeSerializer

class UserPlantedTreeView(LoginRequiredMixin, ListView):
  model = PlantedTree
  template_name = 'trees/user_planted_trees.html'
  context_object_name = 'planted_trees'

  def get_queryset(self):
    return PlantedTree.objects.filter(user=self.request.user)

class AccountPlantedTreeView(LoginRequiredMixin, ListView):
  model = PlantedTree
  template_name = 'trees/account_planted_trees.html'
  context_object_name = 'planted_trees'

  def get_queryset(self):
    user_accounts = self.request.user.accounts.all()
    return PlantedTree.objects.filter(account__in=user_accounts)

class PlantedTreeDetailView(LoginRequiredMixin, DetailView):
  model = PlantedTree
  template_name = 'trees/planted_tree_detail.html'
  context_object_name = 'tree'
  
  def get_object(self, queryset=None):
    obj = super().get_object(queryset)
    user_accounts = self.request.user.accounts.all()
    if obj.account not in user_accounts:
        raise PermissionDenied
    return obj

class PlantedTreeCreateView(LoginRequiredMixin, CreateView):
  model = PlantedTree
  fields = ['tree', 'account', 'age', 'latitude', 'longitude']
  template_name = 'trees/planted_tree_form.html'
  success_url = reverse_lazy('user-trees')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
      
  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    form.fields['account'].queryset = self.request.user.accounts.all()
    return form

class CustomLoginView(LoginView):
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      logout(request)
    
    return super().dispatch(request, *args, **kwargs)

class UserPlantedTreeAPIView(generics.ListAPIView):
  serializer_class = PlantedTreeSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return PlantedTree.objects.filter(user=self.request.user)
  
def custom_page_not_found_view(request, exception):
  return redirect(reverse('login'))
